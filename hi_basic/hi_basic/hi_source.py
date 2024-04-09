#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 15:52:03
FilePath: /hikit/hi_basic/hi_basic/hi_source.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 
'''

import os
import re
import shutil
from .hi_log import *
from .hi_path import *
from .hi_config import *
from .hi_enum import *
from .hi_repo import *


class HiSourceKey(object):
    """For source list key."""

    GROUPS = "group"
    GROUP_NAME = "name"
    GROUP_DESC = "desc"
    APPS = "apps"
    pass


class HiAppGroupInfo(object):
    """Group Info."""

    def __init__(self, info: dict) -> None:
        """Init."""
        self._dict = info
        self._name = info[HiSourceKey.GROUP_NAME]
        self._desc = info[HiSourceKey.GROUP_DESC]
        self._apps = info[HiSourceKey.APPS]
        pass

    @property
    def name(self) -> str:
        """Name."""
        return self._name

    @property
    def desc(self) -> str:
        """Desc."""
        return self._desc

    @property
    def apps(self) -> list:
        """Apps's names. Return type is list[str]."""
        return self._apps

    def to_dict(self) -> dict:
        """For dict."""
        return self._dict
    pass


class HiSourceGroupList(HiConfig):
    """For manager group list."""

    APP_LIST_FILE = "app-list.json"

    def __init__(self, path: str = HiPath.sourcepath()):
        """Init."""
        super().__init__(
            path=os.path.join(path, self.APP_LIST_FILE),
            auto_create=False
            )
        pass

    @property
    def groups(self) -> list:
        """Fetch app groups. Return type is list[HiAppGroupInfo]."""
        groups: list = []
        for info in self.items[HiSourceKey.GROUPS]:
            groups.append(HiAppGroupInfo(info))
        return groups

    def apps_in_group(self, group_name: str) -> list:
        """Fetch apps in group. Return type is list[HiAppInfo]."""
        for info in self.items[HiSourceKey.GROUPS]:
            if info[HiSourceKey.GROUP_NAME] == group_name:
                app_list = []
                for name in info[HiSourceKey.APPS]:
                    app_path = os.path.join(os.path.split(self.path)[0], name + ".json")
                    app_list.append(HiAppInfo(app_path, is_config=True))
                return app_list
        return []

    def check_group_exist(self, name: str) -> bool:
        """Check group exist."""
        for group in self.groups:
            if group.name == name:
                return True
        return False

    def check_app_exist(self, name: str) -> bool:
        """Check group exist."""
        for group in self.groups:
            if name in group.apps:
                return True
        return False

    def add_app(self, name: str, group: str) -> bool:
        """Add a app to config. Return is success."""
        groups = self.groups
        for index in range(0, len(groups)):
            group_info = groups[index]
            if group_info.name == group:
                if name not in group_info.apps:
                    self.writer[HiSourceKey.GROUPS][index][HiSourceKey.APPS] = group_info.apps + [name]
                return True
        return False

    def add_group(self, group: str, desc: str) -> bool:
        """Add a group to config."""
        if self.check_group_exist(group):
            return False

        group_list = self.items[HiSourceKey.GROUPS]
        group_list = group_list + [{
            HiSourceKey.GROUP_NAME: group,
            HiSourceKey.GROUP_DESC: desc,
            HiSourceKey.APPS: []
        }]
        self.writer[HiSourceKey.GROUPS] = group_list
        return True

    def all_apps(self) -> list:
        """List all apps. Return type is list[str]."""
        app_list = []
        for group in self.groups:
            app_list.extend(group.apps)
        return app_list
    pass


class HiSource(object):
    """Used to manager app list."""

    def __init__(self, path: str = HiPath.sourcepath()) -> None:
        """Init."""
        super().__init__()
        self._path = path
        self._group_list = HiSourceGroupList(path=path)
        self._repo = HiRepo(local=path)
        pass

    @property
    def path(self) -> str:
        """Source path."""
        return self._path

    @classmethod
    def setup_source(cls, url: str) -> None:
        """Change source path."""
        cache_path = HiPath.cachepath("source")
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
        HiFile.ensure_dirs(cache_path)
        HiLog.debug("setup source to: " + str(url))
        repo = HiRepo(
            local=os.path.join(cache_path, "source"),
            remote=url)
        repo.transmitter.download()

        if HiSource.check_valid(repo.transmitter.local):
            if os.path.exists(HiPath.sourcepath()):
                shutil.rmtree(HiPath.sourcepath())
            os.rename(repo.transmitter.local, HiPath.sourcepath())
            shutil.rmtree(cache_path)
            # update the app source key.
            HiConfig.hikit_config().writer[HiPath.APP_SOURCE_KEY] = url
        else:
            if os.path.exists(cache_path):
                shutil.rmtree(cache_path)
            raise ValueError("The source is invalid! Please check the format.")
        pass

    @classmethod
    def exist_source(cls) -> bool:
        """Check the source is setup."""
        return True if HiPath.appsource() else False

    @classmethod
    def check_valid(cls, path: str) -> bool:
        """Check the source is valid."""
        app_list_path = os.path.join(path, HiSourceGroupList.APP_LIST_FILE)
        if not HiConfig.exists(app_list_path):
            HiLog.warning(str(app_list_path) + " app-list not exist!")
            return False

        # Check app exist.
        group_list = HiSourceGroupList(path=path)
        for group in group_list.groups:
            for app in group.apps:
                app_info_path = os.path.join(path, app + ".json")
                if not HiConfig.exists(app_info_path):
                    HiLog.warning(str(app_info_path) + " app info not exist!")
                    return False
        return True

    @classmethod
    def download_source(cls, path: str = HiPath.sourcepath(), url: str = HiPath.appsource()) -> None:
        """Update source to a place."""
        repo = HiRepo(local=path, remote=url)
        repo.transmitter.download()
        pass

    def update(self) -> bool:
        """Update this source."""
        self._repo.transmitter.update()
        pass

    def publish(self, info: str = "") -> None:
        """Publish change."""
        self._repo.transmitter.upload(info=info)
        pass

    def add_group(self, name: str, desc: str) -> None:
        """Add a group."""
        self.group_list.add_group(name=name, desc=desc)
        pass

    def add_app(self, app: HiAppInfo, group: str) -> bool:
        """Add a app."""
        if not self.group_list.add_app(name=app.name, group=group):
            return False

        config = HiConfig(HiPath.sourcepath(app.name + ".json"))
        HiLog.debug("save app config to" + config.path)
        config.items = app.items
        return True

    def search(self, regex: str) -> list:
        """Search a app. Return type is list[str]."""
        app_list = []
        pattern = re.compile(regex)
        for group in self.group_list.groups:
            for app in group.apps:
                if pattern.search(app) is not None:
                    app_list.append(app)
        return app_list

    def installed_apps(self) -> list:
        """Get all installed apps. Return type is list[str]."""
        app_list = []
        for app in self.group_list.all_apps():
            install_app = HiAppInfo.from_installed(app)
            if install_app is not None:
                app_list.append(app)
        return app_list

    @property
    def group_list(self) -> HiSourceGroupList:
        """Group list."""
        return self._group_list

    pass

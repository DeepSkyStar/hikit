#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-09 15:55:33
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-23 16:26:56
FilePath: /hikit/hi_basic/hi_basic/hi_app.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from .hi_path import *
from .hi_enum import *
from .hi_config import *


class HiAppInfoKey(object):
    """App info keys."""

    NAME = "name"
    OWNER = "owner"
    CONTACT = "contact"
    DESC = "desc"
    VERSION = "version"
    TYPE = "type"
    REMOTE = "remote"
    DEFAULT_BRANCH = "default_branch"
    IS_DEFAULT = "is_default"
    COMMANDS = "commands"
    RESOURCES = "resources"
    DEPENDENCIES = "dependencies"
    pass


class HiAppType(object):
    """App Type."""

    BASIC = "basic"
    APP = "app"
    FLUTTER = "flutter"
    pass


class HiAppTransMethod(object):
    """Method used to transfer app or other stuff. Default is Git."""

    GIT = "git"
    LOCAL = "local"
    FTP = "ftp"
    HTTP = "http"
    NOT_SUPPORT = "not_support"
    pass


class HiResourceInfoKey(object):
    """App resource infomation key."""

    NAME = "name"
    URL = "url"
    TRANSFER = "transfer"
    pass


class HiResourceInfo(dict):
    """App resource infomation class. For telling people which value is include."""

    @property
    def name(self) -> str:
        """Storage location relative."""
        return self.get(HiResourceInfoKey.NAME)

    @property
    def url(self) -> str:
        """For fetch resource."""
        if HiResourceInfoKey.URL not in self:
            return ""
        return self.get(HiResourceInfoKey.URL)

    @property
    def transfer(self) -> HiAppTransMethod:
        """Transfer method for fetch resource. Default is Git."""
        if HiResourceInfoKey.TRANSFER not in self:
            return HiAppTransMethod.GIT
        if not HiAppTransMethod.include(self.get(HiResourceInfoKey.TRANSFER)):
            return HiAppTransMethod.NOT_SUPPORT
        return HiAppTransMethod(self.get(HiResourceInfoKey.TRANSFER))

    pass


class HiAppInfo(object):
    """App infomation class."""

    def __init__(self, path: str, is_config: bool = False) -> None:
        """Create from the info path.

        Args:
            path (str): The app path.
        """
        if is_config:
            self._config = HiConfig(path=path, auto_create=False)
        else:
            self._config = HiConfig(path=os.path.join(path, "hikit-info.json"), auto_create=False)
        pass

    @classmethod
    def from_source(cls, name: str) -> "HiAppInfo":
        """Fetch app infomation from source list."""
        config_path = os.path.join(HiPath.sourcepath(), name + ".json")
        if not os.path.exists(config_path):
            return None
        return HiAppInfo(path=config_path, is_config=True)

    @classmethod
    def from_installed(cls, name: str) -> "HiAppInfo":
        """Fetch app infomation from installed app."""
        if name == "hi":
            return HiAppInfo(HiPath.libpath("hikit"))
        if not os.path.exists(HiPath.infopath(name=name)):
            return None
        return HiAppInfo(HiPath.libpath(name))

    @classmethod
    def from_local(cls, path: str = os.getcwd()) -> "HiAppInfo":
        """Fetch app information from local path."""
        config_path = os.path.join(path, "hikit-info.json")
        if not os.path.exists(config_path):
            return None
        return HiAppInfo(config_path, is_config=True)

    @property
    def config(self) -> HiConfig:
        return self._config

    @property
    def path(self) -> str:
        return self._config.path

    @property
    def name(self) -> str:
        """Name for app."""
        return self._config[HiAppInfoKey.NAME]

    @property
    def contact(self) ->str:
        """Contact info."""
        return self._config[HiAppInfoKey.CONTACT]

    @property
    def desc(self) -> str:
        """Introduction for app."""
        return self._config[HiAppInfoKey.DESC]

    @property
    def owner(self) -> str:
        """Owner is the maintaner."""
        return self._config[HiAppInfoKey.OWNER]

    @property
    def version(self) -> str:
        """Version for app update."""
        return self._config[HiAppInfoKey.VERSION]

    @property
    def items(self) -> dict:
        return self._config.items

    @property
    def app_path(self) -> str:
        """Return app path."""
        return os.path.split(self.path)[0]

    @property
    def remote(self) -> str:
        """Remote address for app update, only support Git."""
        if self.name == "hikit":
            return HiPath.hikitsource()
        return self._config[HiAppInfoKey.REMOTE]

    @property
    def default_branch(self) -> str:
        """If is empty, will use default."""
        return self._config[HiAppInfoKey.DEFAULT_BRANCH]

    @property
    def type(self) -> HiAppType:
        """Use to define app type."""
        return self._config[HiAppInfoKey.TYPE]

    @property
    def commands(self) -> list:
        """For define multiple commands, must be legal written. Return type is list[str]."""
        if self._config[HiAppInfoKey.COMMANDS] is None:
            return []
        return self._config[HiAppInfoKey.COMMANDS]

    @property
    def dependencies(self) -> list:
        """If dependencies not in the app list, will not work. Return type is list[str]."""
        if self._config[HiAppInfoKey.DEPENDENCIES] is None:
            return []
        return self._config[HiAppInfoKey.DEPENDENCIES]

    @property
    def resources(self) -> list:
        """Use to fetch remote data. Return type is list[HiResourceInfo]."""
        resources = []
        if self._config[HiAppInfoKey.RESOURCES] is None:
            return []
        for info in self._config[HiAppInfoKey.RESOURCES]:
            resources.append(HiResourceInfo(info))
        return resources

    def copy_to(self, path: str):
        """Copy to another place."""
        config = HiConfig(path)
        config.items = self._config.items
        pass

    pass

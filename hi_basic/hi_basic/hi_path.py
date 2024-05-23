#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-12 20:37:40
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-23 19:36:32
FilePath: /hikit/hi_basic/hi_basic/hi_path.py
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

import os
from .hi_log import *
from .hi_file import *
from .hi_config import *


class HiPath(object):
    """Provide important path for hikit."""

    HIKIT_SOURCE_KEY = "hikit_source"
    APP_SOURCE_KEY = "app_source"
    VENV_PATH = "~/.hikit/hienv"

    @classmethod
    def hikitsource(cls) -> str:
        """Remote address for hikit.

        Depends on the first installed.
        """
        return HiConfig.hikit_config()[cls.HIKIT_SOURCE_KEY]

    @classmethod
    def setup_hikitsource(cls, url: str) -> str:
        """Set hikit source."""
        HiConfig.hikit_config().writer[cls.HIKIT_SOURCE_KEY] = url
        pass

    @classmethod
    def appsource(cls) -> str:
        """Remote address for app source.

        Depends on the first open list or update.
        """
        return HiConfig.hikit_config()[cls.APP_SOURCE_KEY]

    @classmethod
    def setup_appsource(cls, url: str) -> str:
        """Set app source."""
        HiConfig.hikit_config().writer[cls.APP_SOURCE_KEY] = url
        pass

    @classmethod
    def sourcepath(cls, path: str = "") -> str:
        """Path for app source git."""
        if path:
            return os.path.join(cls.sourcepath(), path)
        return cls.runpath("source")

    @classmethod
    def runpath(cls, path: str = "") -> str:
        """Path for hikit installed."""
        if path:
            return os.path.join(cls.runpath(), path)
        return HIKIT_PATH

    @classmethod
    def userpath(cls, path: str = "") -> str:
        """Path for hikit user infomations stored."""
        if path:
            return os.path.join(cls.userpath(), path)
        return HIKIT_USERPATH

    @classmethod
    def libpath(cls, path: str = "") -> str:
        """Path for install apps."""
        if path:
            return os.path.join(cls.libpath(), path)
        return cls.runpath("lib")

    @classmethod
    def resourcepath(cls, app: str = "", resource: str = "") -> str:
        """Path for download app resource."""
        path = cls.runpath("resource")
        if app:
            path = os.path.join(path, app)
        if resource:
            path = os.path.join(path, resource)
        return path

    @classmethod
    def binpath(cls, path: str = "") -> str:
        """Path for app command line installation."""
        if path:
            return os.path.join(cls.binpath(), path)
        return cls.runpath("bin")

    @classmethod
    def envpath(cls) -> str:
        """Path for hikit venv path."""
        if not os.path.exists(os.path.expanduser(HiPath.VENV_PATH)):
            return ""
        return os.path.expanduser(HiPath.VENV_PATH)

    @classmethod
    def infopath(cls, name: str = "") -> str:
        """Path for app infomation file. Default is hikit's info."""
        if name:
            return os.path.join(cls.libpath(name), "hikit-info.json")
        return os.path.join(cls.libpath("hikit"), "hikit-info.json")

    @classmethod
    def hikit_libpath(cls, path: str = "") -> str:
        """Path for hikit lib itself."""
        if path:
            return os.path.join(cls.hikit_libpath(), path)
        return cls.libpath("hikit")

    @classmethod
    def templatepath(cls, path: str = "") -> str:
        """Path for template's file store."""
        if path:
            return os.path.join(cls.templatepath(), path)
        return cls.hikit_libpath("template")

    @classmethod
    def cachepath(cls, path: str = "") -> str:
        """Path for save cache."""
        if path:
            return os.path.join(cls.cachepath(), path)
        return cls.runpath(".cache")

    pass


def __hipath_init():
    # initial path
    HiFile.ensure_dirs(HiPath.userpath())
    HiFile.ensure_dirs(HiPath.runpath())
    HiFile.ensure_dirs(HiPath.binpath())
    HiFile.ensure_dirs(HiPath.libpath())
    HiFile.ensure_dirs(HiPath.sourcepath())
    HiFile.ensure_dirs(HiPath.resourcepath())
    HiFile.ensure_dirs(HiPath.cachepath())
    pass


__hipath_init()

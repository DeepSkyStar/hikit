#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-09 15:55:33
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-22 21:21:04
FilePath: /hikit/hi_basic/hi_basic/hi_config.py
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
import json
import weakref
from .hi_log import *
from .hi_file import *


class _HiConfigWriter(object):
    def __init__(self, config: "HiConfig", parent: "_HiConfigWriter" = None, key=None, is_autofill=False):
        self._config = config
        self._parent = parent
        self._is_autofill = is_autofill
        self._key = key
        pass

    @property
    def key(self): return self._key

    @property
    def value(self):
        if self._parent is None:
            return self._config.items
        return self._parent.value[self._key]

    @property
    def autofill(self) -> "_HiConfigWriter":
        return _HiConfigWriter(
            self._config,
            parent=self._parent,
            key=self._key,
            is_autofill=True)

    @property
    def a(self) -> "_HiConfigWriter": return self.autofill

    def _autofill_check(self, key):
        if not self._is_autofill:
            return None

        if self._parent is None:
            if key not in self.value:
                self.value[key] = {}
                self._config._save_config()
            return None

        if isinstance(self.value, dict) and key not in self.value:
            self.value[key] = {}
            self._config._save_config()
        pass

    def __getitem__(self, key):
        self._autofill_check(key)
        return _HiConfigWriter(
            config=self._config,
            parent=self,
            key=key,
            is_autofill=self._is_autofill)

    def __setitem__(self, key, value):
        self.value[key] = value
        self._config._save_config()
        pass

    def __delitem__(self, key):
        del self.value[key]
        self._config._save_config()
        pass
    pass


class HiConfig(object):
    """
    For Persistent Data which like apple's UserDefault.

    config = HiConfig("filepath")
    config.writer["key"] = "value"
    print(config["key"])

    the key-value will store in the file.

    Args:
        USER_CONFIG_PATH (str): The default user config path.

    NOTE:
        1. Items will update automatic when file change.
        2. The same file will be the same instance.
    """

    HIKIT_CONFIG_PATH = os.path.join(HIKIT_PATH, HIKIT_CONFIG_NAME)
    USER_CONFIG_PATH = os.path.join(HIKIT_USERPATH, HIKIT_CONFIG_NAME)
    _configs = {}

    def __new__(cls, *args, **kwargs):
        """Make sure the same file will be the same instance."""
        if not args:
            if "path" in kwargs:
                path = kwargs["path"]
            else:
                path = HiConfig.USER_CONFIG_PATH
        else:
            path = args[0]

        # Use weakref to save object.
        if path not in cls._configs or cls._configs[path]() is None:
            config = super().__new__(cls)
            cls._configs[path] = weakref.ref(config)
        else:
            config = cls._configs[path]()

        return config

    def __init__(self, path: str = USER_CONFIG_PATH, editable: bool = True, auto_create: bool = True):
        """HiConfig() will create from ~/.hikit_user/.hiconfig.json .

        Args:
            path (str, optional): The json file path. Defaults to USER_CONFIG_PATH.
            editable (bool, optional): As the name. Defaults to True.
        """
        super().__init__()
        self._path = os.path.abspath(path)
        self._auto_create = auto_create
        self._editable = editable
        if not hasattr(self, "_HiConfig_items"):
            self._items = {}
            self._filestamp = HiFileStamp(self._path)
            self._load_config()
        pass

    @classmethod
    def hikit_config(cls) -> "HiConfig":
        """Config for hikit, PLEASE DO NOT MODIFY BY HAND."""
        return HiConfig(HiConfig.HIKIT_CONFIG_PATH)

    @classmethod
    def app_config(cls, app_name: str) -> "HiConfig":
        """Create or fetch app config."""
        app_userpath = os.path.join(HIKIT_USERPATH, app_name)
        if os.path.exists(app_userpath) and not os.path.isdir(app_userpath):
            raise IOError("Create failed!" + app_userpath + " already exist file!")
        if not os.path.exists(app_userpath):
            os.mkdir(app_userpath)
        return HiConfig(os.path.join(app_userpath, "config.json"))

    @classmethod
    def exists(cls, path: str) -> bool:
        """If the json file exist will return true."""
        if not os.path.exists(path) or not os.path.isfile(path):
            return False

        with open(path, "r", encoding="utf-8") as jsonfile:
            try:
                json.load(jsonfile)
            except ValueError:
                return False

        return True

    @property
    def path(self) -> str:
        """Json file path."""
        return self._path

    @property
    def items(self) -> dict:
        """Items in json will automatic update when file change."""
        if self._filestamp.is_changed:
            self._load_config()
        return self._items

    @items.setter
    def items(self, items: dict):
        """Update items will save into the file immediatly."""
        self._items.update(items)
        self._save_config()
        pass

    @property
    def writer(self) -> _HiConfigWriter:
        """
        For write data into the json file.

        SAMPLE:
            config.writer["abc"] = "test"

        If you want to autofill the middle keys, can use that:
            config.writer.autofill["a"]["b"]["c"] = "test"

        Also provide shotcut write like:
            config.w.a["a"]["b"]["c"] = "test"

        NOTE:
            Please don't ref the writer in other place,
            the behavior will be unpredictable.

        Returns:
            _HiConfigWriter: the writer
        """
        return _HiConfigWriter(self) if self._editable else None

    @property
    def w(self) -> _HiConfigWriter:
        """As same as writer."""
        return self.writer

    def reset(self):
        """Reset the json file."""
        self._init_config()

    def _init_config(self):
        self._items = {}
        self._save_config()
        HiLog.debug("Reset config " + self._path)
        pass

    def _load_config(self):
        if not os.path.exists(self._path):
            if self._auto_create:
                HiFile.ensure_dirs(os.path.split(self._path)[0])
                self._init_config()
        else:
            HiLog.debug(f"Load config {self._path}")
            with open(self._path, "r", encoding="utf-8") as jsonfile:
                try:
                    self._items = json.load(jsonfile)
                    self._filestamp.update()
                except ValueError:
                    HiLog.warning(f"Config {self._path} broken...")
        pass

    def _save_config(self):
        with open(self._path, "w", encoding="utf-8") as jsonfile:
            json.dump(self._items, jsonfile, indent=4, ensure_ascii=False)
        self._filestamp.update()

    def __getitem__(self, key):
        """As same as dict."""
        if self._filestamp.is_changed:
            self._load_config()
        if key in self._items:
            value = self._items[key]
            return value
        return None

    def __iter__(self):
        """As same as dict."""
        return iter(self.items)

    def __contains__(self, item):
        """As same as dict."""
        if item in self.items:
            return True
        return False

    def __len__(self):
        """As same as dict."""
        return len(self._items)

    pass





if __name__ == "__main__":
    config = HiConfig()
    config2 = HiConfig()
    HiLog.info(id(config) == id(config2))
    configdict = {}

    custom_config = HiConfig("test_config.json")
    custom_config["test"] = "1234"

    custom_config2 = HiConfig("test_config.json")
    HiLog.info(custom_config2["test"])

    test_config = HiConfig("test_config.json")
    test_config.update_items({
        "a": "123",
        "b": "1234",
    })

    test_config = HiConfig("test_config.json")
    test_config.w.a[1][2][3][4][5][6][7][8][9] = 10
    pass

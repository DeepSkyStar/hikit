#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 15:53:15
FilePath: /hikit/hi_basic/hi_basic/hi_config.py
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
import json
import weakref
from .hi_log import *
from .hi_file import *


class _HiConfigWriter(object):
    def __init__(self, config: "HiConfig", parent: "_HiConfigWriter" = None, key=None, is_autofill=False):
        self.__config = config
        self.__parent = parent
        self.__is_autofill = is_autofill
        self.__key = key
        pass

    @property
    def key(self): return self.__key

    @property
    def value(self):
        if self.__parent is None:
            return self.__config.items
        return self.__parent.value[self.__key]

    @property
    def autofill(self) -> "_HiConfigWriter":
        return _HiConfigWriter(
            self.__config,
            parent=self.__parent,
            key=self.__key,
            is_autofill=True)

    @property
    def a(self) -> "_HiConfigWriter": return self.autofill

    def __autofill_check(self, key):
        if not self.__is_autofill:
            return None

        if self.__parent is None:
            if key not in self.value:
                self.value[key] = {}
                self.__config._save_config()
            return None

        if isinstance(self.value, dict) and key not in self.value:
            self.value[key] = {}
            self.__config._save_config()
        pass

    def __getitem__(self, key):
        self.__autofill_check(key)
        return _HiConfigWriter(
            config=self.__config,
            parent=self,
            key=key,
            is_autofill=self.__is_autofill)

    def __setitem__(self, key, value):
        self.value[key] = value
        self.__config._save_config()
        pass

    def __delitem__(self, key):
        del self.value[key]
        self.__config._save_config()
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
    __configs = {}

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
        if path not in cls.__configs or cls.__configs[path]() is None:
            config = super().__new__(cls)
            cls.__configs[path] = weakref.ref(config)
        else:
            config = cls.__configs[path]()

        return config

    def __init__(self, path: str = USER_CONFIG_PATH, editable: bool = True, auto_create: bool = True):
        """HiConfig() will create from ~/.hikit_user/.hiconfig.json .

        Args:
            path (str, optional): The json file path. Defaults to USER_CONFIG_PATH.
            editable (bool, optional): As the name. Defaults to True.
        """
        super().__init__()
        self.__path = os.path.abspath(path)
        self.__auto_create = auto_create
        self.__editable = editable
        if not hasattr(self, "_HiConfig__items"):
            self.__items = {}
            self.__filestamp = HiFileStamp(self.__path)
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

        with open(path, "r") as jsonfile:
            try:
                json.load(jsonfile)
            except ValueError:
                return False

        return True

    @property
    def path(self) -> str:
        """Json file path."""
        return self.__path

    @property
    def items(self) -> dict:
        """Items in json will automatic update when file change."""
        if self.__filestamp.is_changed:
            self._load_config()
        return self.__items

    @items.setter
    def items(self, items: dict):
        """Update items will save into the file immediatly."""
        self.__items.update(items)
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
        return _HiConfigWriter(self) if self.__editable else None

    @property
    def w(self) -> _HiConfigWriter:
        """As same as writer."""
        return self.writer

    def reset(self):
        """Reset the json file."""
        self._init_config()

    def _init_config(self):
        self.__items = {}
        self._save_config()
        HiLog.debug("Reset config " + self.__path)
        pass

    def _load_config(self):
        if not os.path.exists(self.__path):
            if self.__auto_create:
                HiFile.ensure_dirs(os.path.split(self.__path)[0])
                self._init_config()
        else:
            with open(self.__path, "r") as jsonfile:
                try:
                    self.__items = json.load(jsonfile)
                    self.__filestamp.update()
                    HiLog.debug(f"Load config {self.__path}")
                except ValueError:
                    HiLog.warning(f"Config {self.__path} broken...")
        pass

    def _save_config(self):
        with open(self.__path, "w") as jsonfile:
            json.dump(self.__items, jsonfile, indent=4)
        self.__filestamp.update()

    def __getitem__(self, key):
        """As same as dict."""
        if self.__filestamp.is_changed:
            self._load_config()
        if key in self.__items:
            value = self.__items[key]
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
        return len(self.__items)

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

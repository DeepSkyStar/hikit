#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-09 15:55:33
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-04 18:25:53
FilePath: /hikit/hi_basic/hi_basic/hi_file.py
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

import hashlib
import os
from .hi_log import *


class HiFileStamp(object):
    """Used to check the file was changed or not."""

    def __init__(self, path: str, simple_check: bool = True) -> None:
        """When simple_check is False, it will generate md5, heavy cost.

        Args:
            path (str): the file path.
            simple_check (bool, optional): Check the file critical. Defaults to True.
        """
        super().__init__()
        self.__simple_check = simple_check
        self.__path = path
        self.__md5 = None
        self.__size = 0
        self.update()
        pass

    @property
    def is_changed(self):
        """Is the file changed."""
        is_exist = os.path.exists(self.__path)
        # exist change.
        if is_exist != self.__is_exist:
            return True
        elif not is_exist:
            return False

        # File change to other stuff.
        is_file = os.path.isfile(self.__path)
        if is_file != self.__is_file:
            return True

        # File time change.
        mtime = os.stat(self.__path).st_mtime
        if mtime != self.__mtime:
            return True

        # Size change.  
        if is_file:
            size = os.path.getsize(self.__path)
            if size != self.__size:
                return True

            # Content change.
            if not self.__simple_check:
                return self.__md5 != hashlib.md5(open(self.__path).read()).hexdigest()

        return False

    def update(self):
        """Update the file stamp to newest."""
        self.__is_exist = os.path.exists(self.__path)
        if not self.__is_exist:
            self.__is_file = False
            self.__size = 0
            self.__md5 = None
            return None

        self.__mtime = os.stat(self.__path).st_mtime
        self.__is_file = os.path.isfile(self.__path)

        if self.__is_file:
            self.__size = os.path.getsize(self.__path)

            if not self.__simple_check:
                self.__md5 = hashlib.md5(open(self.__path).read()).hexdigest()
        pass
    pass


class HiFile(object):
    """For some convenient file operations."""

    @classmethod
    def ensure_dirs(cls, path: str, should_exit: bool = True) -> bool:
        """For ensure some dirs is exist, if not, will create automatically.

        If create failed, will raise IOError.

        Args:
            path (str): the path which you want to ensure
            should_exit (bool, optional): When create failed is will raise IOError. Defaults to True.

        Returns:
            bool: success or not.
        """
        try_path = os.path.abspath(path)
        make_dirs = []
        while not os.path.exists(try_path):
            make_dirs.append(try_path)
            try_path = os.path.dirname(try_path)

        if not os.path.isdir(try_path):
            HiLog.critical(try_path + "Create dir failed! Because there is a file!")
            if should_exit:
                raise IOError("Create dir failed! Because there is a file!")
            else:
                return False

        make_dirs.reverse()
        for dirname in make_dirs:
            os.mkdir(dirname)

        if make_dirs:
            HiLog.debug(path + " create success.")
        return True

    @classmethod
    def find_first(
        cls,
        name: str,
        path: str = os.getcwd(),
        is_dir: bool = True,
        recursive: bool = True,
        should_exit: bool = True
            ) -> str:
        """Find the first dir or file recursive util root."""
        if not os.path.exists(path):
            if should_exit:
                raise IOError("The finding path is not exists.")
            return ""

        if not os.path.isdir(path):
            if should_exit:
                raise IOError("The finding path is not a dir.")
            return ""

        while path:
            checking_path = os.path.join(path, name)
            if os.path.exists(checking_path):
                if os.path.isdir(checking_path) == is_dir:
                    return checking_path
            if path == "/":
                return ""
            path = os.path.split(path)[0]

        return ""

    pass

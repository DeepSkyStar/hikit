#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-09 15:55:33
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-22 21:03:21
FilePath: /hikit/hi_basic/hi_basic/hi_sys.py
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
import sys
import select
import platform
import contextlib
import pathlib
from .hi_log import *
from .hi_path import *


class _HiSys(object):
    """Use to provide more function for multiple system."""

    _PATH_CONTENT = """
# Setting PATH for hikit
export hikit_BIN="<BIN_PATH>"
export PATH="${PATH}:${hikit_BIN}"
"""

    def __init__(self) -> None:
        pass

    def setup_path(self, content: str = _PATH_CONTENT, bin_path: str = HiPath.binpath()) -> None:
        """Makesure the bin path is correct. bin_path will replace <BIN_PATH> in content."""
        raise SystemError("Current system is not support!")

    def get_key(self) -> str:
        raise SystemError("Current system is not support!")

    def to_bash(self, command: str) -> str:
        return "/bin/bash -c \"" + command + "\""

    pass


"""Provide a global var for sys call."""
HiSys: _HiSys = None


class _HiSysMacOS(_HiSys):
    """For macOS user."""

    def __init__(self) -> None:
        super().__init__()

        pass

    def setup_path(self, content: str = _HiSys._PATH_CONTENT, bin_path: str = HiPath.binpath()) -> None:
        profiles = [
            os.path.join(os.path.expanduser('~'), ".bash_profile"),
            os.path.join(os.path.expanduser('~'), ".bashrc"),
            os.path.join(os.path.expanduser('~'), ".zprofile")
        ]

        no_zprofile = False

        for profile in profiles:
            if os.path.exists(profile):
                HiLog.debug("Found profile " + profile)
                self._setup_pathfile(
                    profilepath=profile,
                    content=content,
                    bin_path=bin_path)
            elif os.path.split(profile)[1] == ".zprofile":
                no_zprofile = True
            pass

        if no_zprofile:
            self._setup_pathfile(
                profilepath=os.path.join(os.path.expanduser('~'), ".zshrc"),
                content=content,
                bin_path=bin_path,
                is_force=True)
        pass

    def get_key(self) -> str:
        # TODO: Not very work, should figure out later.
        HiLog.debug("Fetch key.")
        with self.__raw_mode(sys.stdin):
            HiLog.debug("Detect input.")
            x = select.select([sys.stdin], [], [], 0)[0]
            print(x)
            if sys.stdin not in x:
                return ""
            HiLog.debug("Fetch input.")
            ch = sys.stdin.read(1)
            HiLog.debug("Finished input.")
            return ch

    @contextlib.contextmanager
    def __raw_mode(self, file):
        # old_attrs = termios.tcgetattr(file.fileno())
        # new_attrs = old_attrs[:]
        # new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
        # try:
        #     termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        #     yield
        # finally:
        #     termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)
        yield
        pass

    def _setup_pathfile(self, profilepath: str, content: str, bin_path: str, is_force: bool = False):
        if not os.path.exists(profilepath):
            if is_force:
                pathlib.Path(profilepath).touch()
            else:
                HiLog.debug(profilepath + " NOT Found.")
                return None
        profilecontent = ""
        with open(profilepath, "r", encoding="utf-8") as pathfile:
            profilecontent = pathfile.read()

        if profilecontent.find(bin_path) == -1:
            path_temp = content.replace("<BIN_PATH>", bin_path)
            profilecontent = profilecontent + "\n" + path_temp
            with open(profilepath, "w", encoding="utf-8") as pathfile:
                pathfile.write(profilecontent)

        os.system(self.to_bash("source " + profilepath))
        pass

    pass


class _HiSysLinux(_HiSysMacOS):
    """For linux user. As same as mac."""

    pass


class _HiSysWindows(_HiSys):
    """For windows user."""

    def __init__(self) -> None:
        super().__init__()
        pass

    def setup_path(self, content: str = _HiSys._PATH_CONTENT, bin_path: str = HiPath.binpath()) -> None:
        raise SystemError("DO NOT SUPPORT WINDOWS YET!")

    def get_key(self) -> str:
        import msvcrt
        if msvcrt.kbhit():
            return msvcrt.getch()
        else:
            return ""
    pass


def __init_sys():
    global HiSys
    if HiSys is None:
        system = platform.system()
        if system == "Darwin":
            HiSys = _HiSysMacOS()
        elif system == "Windows":
            HiSys = _HiSysWindows()
        elif system == "Linux":
            HiSys = _HiSysLinux()
        else:
            HiSys = _HiSys()
    pass


__init_sys()

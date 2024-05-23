#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-09 15:55:33
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-23 17:48:22
FilePath: /hikit/hi_basic_setup.py
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


# Before install other staff, must be ensure hi_basic already installed.
def install_pip_module(path: str):
    """Install the python module."""
    lastpath = os.getcwd()

    os.chdir(path)
    print("Clear all existing installation packages...")
    distpath = os.path.join(path, "dist")
    os.system("rm -r " + distpath)
    print("Starting to generate new installation packages...")
    setupfile = os.path.join(path, "setup.py")
    os.system("python3 " + setupfile + " sdist")
    distlist = os.listdir(distpath)
    os.chdir(distpath)
    print("Starting install " + distlist[0] + "...")
    if sys.prefix == os.path.expanduser("~/.hikit/hienv"):
        os.system("python3 -m pip install " + distlist[0])
    else:
        os.system("python3 -m pip install --user " + distlist[0])
    os.chdir(lastpath)
    pass


def install_basic():
    """Install basic module."""
    curdir = os.path.dirname(os.path.abspath(__file__))
    print("Current directory is:", curdir)
    basicpath = os.path.join(curdir, "hi_basic")
    print("hi_basic path is:", basicpath)
    install_pip_module(basicpath)
    pass


if __name__ == "__main__":
    install_basic()
    pass

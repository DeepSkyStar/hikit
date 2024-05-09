#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-09 15:42:14
FilePath: /hikit/hi_basic/hi_basic/hi_tranmitter/hi_transmitter.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 
'''

from collections.abc import Callable
from typing import Any

# HiTransferResultCallback = Callable[[Any, Any], None]
HiTransferResultCallback = Callable


class HiTransmitter(object):
    """Use to transfer data."""

    def __init__(self, local: str, remote: str, info: dict) -> None:
        self._local = local
        self._remote = remote
        self._info = info
        pass

    @property
    def local(self) -> str: return self._local

    @property
    def remote(self) -> str: return self._remote

    @property
    def info(self) -> str: return self._info

    def download(self) -> None:
        raise ValueError(type(self).__name__ + " not support download Yet!")

    def upload(self, info: str = "") -> None: 
        raise ValueError(type(self).__name__ + " not support upload Yet!")

    def update(self, branch: str = None) -> None:
        raise ValueError(type(self).__name__ + " not support update Yet!")

    def switch(self, version: str) -> None:
        raise ValueError(type(self).__name__ + " not support switch Yet!")

    pass
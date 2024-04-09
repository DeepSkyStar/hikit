#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 15:53:05
FilePath: /hikit/hi_basic/hi_basic/hi_enum.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 
'''

from enum import Enum


class HiStrEnum(Enum):
    """To make it easier to manipulate string enum."""

    @classmethod
    def include(cls, v) -> bool:
        """Check valid."""
        return v in cls._value2member_map_
    pass

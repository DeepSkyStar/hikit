#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-12 20:37:40
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-04 18:27:12
FilePath: /hikit/hi_basic/hi_basic/hi_text.py
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
import gettext
from .hi_log import *
from .hi_config import *


def HiText(key: str, text: str = "") -> str:
    """Hi Str for translate."""
    if text:
        return text
    return key


class HiTextManager(object):
    """For easy multi language."""

    def __init__(self) -> None:
        super().__init__()
        pass

    def select(self, lang: str = "") -> bool:
        return False

    def support_list(self) -> list:
        """Return type is list[str]."""
        return []

    pass

#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-12 20:37:40
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-11 00:52:13
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
import inspect
from .hi_log import *
from .hi_config import *
from .hi_multilang import *

__hi_text_dict = {}

def HiText(key: str, text: str = "") -> str:
    """Hi Str for translate."""
    stack = inspect.stack()
    caller_info = stack[1]
    filepath = caller_info[1]

    global __hi_text_dict
    if filepath in __hi_text_dict:
        lang = __hi_text_dict[filepath]
        if isinstance(lang, HiMultiLang):
            return lang.get_text(filepath, key)
        elif text:
            return text
    else:
        langpath = HiMultiLang.find_lang_file(os.path.dirname(filepath))
        if langpath:
            lang = HiMultiLang(os.path.dirname(langpath))
            __hi_text_dict[filepath] = lang
            return lang.get_text(filepath, key)
        else:
            __hi_text_dict[filepath] = ""

    if text:
        return text
    return key

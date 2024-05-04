#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-09 15:55:33
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-04 18:25:26
FilePath: /hikit/hi_basic/hi_basic/hi_cipher.py
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

import abc
import base64


class HiCipherMethod(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def encode(self) -> str: return None

    @abc.abstractmethod
    def decode(self) -> str: return None
    pass


class HiCipherMethodBase64(HiCipherMethod):
    def encode(self) -> str:
        return base64.b64encode(str)

    def decode(self) -> str:
        return base64.b64decode(str)

    pass


class HiCipher(object):
    @classmethod
    def encode(cls, data, method: HiCipherMethod) -> str:
        return method.encode(data)

    @classmethod
    def decode(cls, data, method: HiCipherMethod = None) -> str:
        # TODO: Add method selector here.
        return method.decode(data)

    pass

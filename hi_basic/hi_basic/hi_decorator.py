#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-09 15:55:33
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-04 18:25:37
FilePath: /hikit/hi_basic/hi_basic/hi_decorator.py
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

from functools import wraps
from .hi_log import *


class limitedby(object):
    """limitedby decorator.

    used to limit function call. If any condition not true, will raise ValueError and tips which one are false.

    SAMPLE:

        @limitedby(isinited, readable)
        def func():

    for above sample, when isinited or readable is False, the func will not be call, and process will exit.

    NOTICE:

        1. Can support multiple conditions.
        2. The condition must be class var or property, the property's value depends on the value of the instance.
    """

    @staticmethod
    def __void_func(*args, **kwargs):
        return None

    def __init__(self, *args):
        self.__hi_conditions = args

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            count = 0
            for condition in self.__hi_conditions:
                count = count + 1
                if type(condition) is property:
                    condition = condition.fget(args[0])
                if not condition:
                    HiLog.critical(f"{str(func)} call failed, condition <{str(count)}> (start from 1) is False!")
                    raise ValueError(f"{str(func)} call failed, condition <{str(count)}> (start from 1) is False!")
                    return limitedby.__void_func
            return func(*args, **kwargs)
        return wrapped_function
    pass


if __name__ == "__main__":
    condition1 = True
    condition2 = False

    @limitedby(condition1, condition2)
    def __test_function(teststr: str = "This is a test"):
        HiLog.info(teststr)
        pass

    __test_function()
    pass

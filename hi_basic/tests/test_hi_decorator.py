#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 15:51:41
FilePath: /hikit/hi_basic/tests/test_hi_decorator.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 
'''

import unittest
import sys
import os
if "hi_basic" not in sys.modules:
    sys.path.append(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
    from hi_basic import *


class TestHiDecorator(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        return super().tearDown()

    def test_sample(self):
        condition1 = True
        condition2 = False

        @limitedby(condition1, condition2)
        def __test_function(teststr: str = "This is a test"):
            HiLog.info(teststr)
            pass

        __test_function()
        pass
    pass


if __name__ == "__main__":
    unittest.main()
    pass

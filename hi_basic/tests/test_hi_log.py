#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-09 15:55:33
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-04 18:27:29
FilePath: /hikit/hi_basic/tests/test_hi_log.py
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

import unittest
import sys
import os
if "hi_basic" not in sys.modules:
    sys.path.append(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
    from hi_basic import *


class _TestHiLog(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        return super().tearDown()

    def test_sample(self):
        HiLog.debug('debug print')
        HiLog.info('info print')
        HiLog.warning('warning print')
        HiLog.error('error print')
        HiLog.critical('critical print')
        HiLog.debug('%s customer print' % 'these things')
        pass

    pass


if __name__ == "__main__":
    unittest.main()
    pass

#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-09 15:55:33
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-04 18:25:58
FilePath: /hikit/hi_basic/hi_basic/hi_lock.py
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

from collections.abc import Callable


class HiLock(object):
    """For doing operations after lock."""

    def __init__(self) -> None:
        """For easy make some bootstrap."""
        self._run_list = []
        self._is_locked = False
        pass

    @property
    def is_locked(self):
        """Lock state."""
        return self._is_locked

    def run(self, operation: Callable) -> bool:
        """Run operation later until unlock. operation type is: Callable[[None], None]."""
        if self._is_locked:
            self._run_list.append(operation)
            return False
        operation()
        return True

    def lock(self):
        """Just set to lock."""
        self._is_locked = True
        pass

    def unlock(self):
        """When unlock, will run all the oprations during lock."""
        if self._is_locked:
            run_list = self._run_list
            self._run_list = []
            for operation in run_list:
                operation()
            self._is_locked = False
        pass

    pass

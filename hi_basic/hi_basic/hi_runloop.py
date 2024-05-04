#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-09 15:55:33
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-04 18:26:56
FilePath: /hikit/hi_basic/hi_basic/hi_runloop.py
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

import time
import weakref
from collections.abc import Callable
from typing import Any
from .hi_lock import *


"""The param is the runloop"""
# HiRunloopBlock = Callable[["HiRunloop"], None]
HiRunloopBlock = Callable

"""The param is the observer"""
# HiObserverBlock = Callable[["HiObserver"], None]
HiObserverBlock = Callable


class HiObserver(object):
    """Use to define a observer."""

    def __init__(self) -> None:
        """Must be call in subclass."""
        self._runloop = None
        pass

    @property
    def runloop(self) -> "HiRunloop":
        """Runloop for observer."""
        return self._runloop() if self._runloop is not None else None

    def _check(self) -> bool:
        return False

    def _run(self) -> None:
        """Override."""
        pass

    pass


class HiRunloop(object):
    """For lightly make async operation."""

    __runloops = {}

    def __new__(cls, *args, **kwargs) -> None:
        """Make sure the same file will be the same instance."""
        if not args:
            if "name" not in kwargs:
                name = "main"
            else:
                name = kwargs["name"]
        else:
            name = args[0]
        # After create, runloop will not release.
        if name not in cls.__runloops:
            runloop = super().__new__(cls)
            cls.__runloops[name] = runloop
        else:
            runloop = cls.__runloops[name]
        return runloop

    def __init__(
            self,
            name: str = "main",
            tick: float = 1.0/10000,
            ) -> None:
        """Init a runloop.

        Args:
            name (str, optional): the name for identify a runloop, same name same object. Defaults to "main".
            tick (float, optional): the minimum tick for each running. Defaults to 1.0/10000 seconds.
        """
        super().__init__()
        self._name = name
        self._tick = tick
        self._is_running = False
        self._observer_lock = HiLock()
        self._start_timestamp = 0.0
        self._last_timestamp = 0.0
        # Type is list[HiObserver]
        self._observer_list: list = []
        # Type is list[tuple[HiRunloopBlock, float]]
        self._pending_list: list = []
        pass

    @classmethod
    def from_name(cls, name: str) -> "HiRunloop":
        """Get runloop by name."""
        return cls.__runloops[name]

    @property
    def name(self) -> bool:
        """Return name for identify a runloop."""
        return self._name

    @property
    def is_running(self) -> bool:
        """Return the state whether is running."""
        return self._is_running

    @property
    def running_time(self) -> bool:
        """Return running time since start."""
        return self._last_timestamp - self._start_timestamp

    def start(self, immediately: bool = False) -> None:
        """Start the runloop."""
        if self._is_running:
            return None
        self._is_running = True
        self._start_timestamp = time.time()
        self._last_timestamp = self._start_timestamp
        if not immediately:
            time.sleep(self._tick)
        self._runloop()
        pass

    def stop(self) -> None:
        """Stop the runloop."""
        self._is_running = False
        pass

    def async_run(self, block: HiRunloopBlock, after: float = 0.0) -> None:
        """For do some async operation.

        Args:
            block (HiRunloopBlock): the exec func
            after (float, optional): run block after seconds. Defaults to 0.0.
        """
        self._pending_list.append([block, after])
        pass

    def add_observer(self, observer: "HiObserver") -> None:
        """Add a observer to runloop."""
        self._observer_lock.run(
            lambda weakself=weakref.ref(self), ob=observer:
                weakself()._add_observer(ob) if weakself() is not None else None
            )
        pass

    def _add_observer(self, observer: "HiObserver") -> None:
        self._observer_list.append(observer)
        observer._runloop = weakref.ref(self)
        pass

    def del_observer(self, observer: "HiObserver") -> None:
        """Del the observer to runloop."""
        self._observer_lock.run(
            lambda weakself=weakref.ref(self), ob=observer:
                weakself()._del_observer(ob) if weakself() is not None else None
            )
        pass

    def _del_observer(self, observer: "HiObserver") -> None:
        self._observer_list.remove(observer)
        observer._runloop = None
        pass

    def del_all_observers(self) -> None:
        """Del all the observers."""
        self._observer_lock.run(
            lambda weakself=weakref.ref(self):
                weakself()._observer_list.clear() if weakself() is not None else None
            )
        pass

    def _runloop(self) -> None:
        while self._is_running:
            time.sleep(self._tick)
            last_timestamp = self._last_timestamp
            self._last_timestamp = time.time()

            self._observer_lock.lock()
            # Check the observers.
            for observer in self._observer_list:
                if observer._check():
                    observer._run()

            self._observer_lock.unlock()

            # call the pending list.
            pending_list = []
            while len(self._pending_list) > 0:
                block, after = self._pending_list[0]
                delta = time.time() - last_timestamp
                del self._pending_list[0]
                if after >= last_timestamp:
                    block(self)
                else:
                    pending_list.append((block, after - delta))
            self._pending_list.extend(pending_list)
        pass

    pass

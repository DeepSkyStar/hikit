#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 15:51:48
FilePath: /hikit/hi_basic/hi_basic/hi_timer.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 
'''

import time
from collections.abc import Callable
from typing import Any
from .hi_runloop import *

"""First param is the observer, Second param is the delta time."""
# HiTimerBlock = Callable[["HiTimer", float], None]
HiTimerBlock = Callable


class HiTimer(HiObserver):
    """For running a func period."""

    def __init__(self, block: HiTimerBlock) -> None:
        super().__init__()
        """For running a func period."""
        self._block = block
        self._interval = 0.0
        self._last_timestamp = 0.0
        pass

    @property
    def interval(self) -> float:
        """Interval when timer run."""
        return self._interval

    @property
    def last_timestamp(self) -> float:
        """Last timestamp."""
        return self._last_timestamp

    @classmethod
    def perform(
            cls,
            block: HiTimerBlock,
            runloop: HiRunloop = HiRunloop(),
            interval: float = 0.1,
            immediatly: bool = False) -> "HiTimer":
        """For quick to use."""
        timer = HiTimer(block)
        timer.start_run(runloop=runloop, interval=interval, immediatly=immediatly)
        return timer

    def start_run(
            self,
            runloop: HiRunloop,
            interval: float = 0.1,
            immediatly: bool = False,
            ) -> None:
        """Start runing.

        Args:
            performer (HiTimerRunner): the timer runner.
            interval (float, optional): the interval for run, for performence do not lower than 0.001. Defaults to 0.1.
            immediatly (bool, optional): _description_. Defaults to False.
        """
        self.stop_run()
        self._last_timestamp = time.time()
        self._interval = interval
        runloop.add_observer(self)
        if immediatly:
            self._block(self, 0.0)
        pass

    def stop_run(self) -> None:
        """Stop timer will remove the timer from runner."""
        self.runloop.del_observer(self)
        pass

    def _check(self) -> bool:
        return time.time() - self._last_timestamp >= self._interval

    def _run(self) -> None:
        """For timer exec."""
        last_timestamp = time.time()
        time_delta = last_timestamp - self._last_timestamp
        self._block(self, time_delta)
        self._last_timestamp = last_timestamp
        pass

    pass

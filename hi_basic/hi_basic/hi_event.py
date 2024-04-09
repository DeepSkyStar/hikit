#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 15:53:01
FilePath: /hikit/hi_basic/hi_basic/hi_event.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 
'''

import weakref
from collections.abc import Callable
from typing import Any
from .hi_runloop import *
from .hi_lock import *

"""The first object is event receiver, second is the event, last is event's info."""
# HiEventBlock = Callable[["HiEventReceiver", str, Any], None]
HiEventBlock = Callable


class HiEventReceiver(object):
    """For receive event and process."""

    def __init__(self, event: str, block: HiEventBlock) -> None:
        """For init a event receiver."""
        self._receiving_event = event
        self._block = block
        pass

    def receive_event(self, event: str, info: Any):
        """Receive event."""
        if self._receiving_event == event:
            self._block(self, event, info)
        pass
    pass


class HiEventReceiver(object):
    """For receive event and process."""

    def __init__(self, event: str, block: HiEventBlock) -> None:
        """For init a event receiver."""
        self._receiving_event = event
        self._block = block
        pass

    def receive_event(self, event: str, info: Any):
        """Receive event."""
        if self._receiving_event == event:
            self._block(self, event, info)
        pass
    pass


class HiEventCenter(HiObserver):
    """Used to dispatch event."""

    __shared_object = None

    def __init__(self) -> None:
        """Init."""
        self._receiver_lock = HiLock()
        # Type is list[HiEventReceiver].
        self._reicevers: list = []
        self._event_lock = HiLock()
        # Type is list[(str, Any)].
        self._pending_events: list = []
        pass

    @classmethod
    def shared(cls) -> "HiEventCenter":
        """Shared global center."""
        if cls.__shared_object is None:
            cls.__shared_object = HiEventCenter()
        return cls.__shared_object

    def send(self, event: str, info: Any) -> None:
        """Send event."""
        self._receiver_lock.lock()
        for receiver in self._reicevers:
            receiver.receive_event(event=event, info=info)
        self._receiver_lock.unlock()
        pass

    def send_async(self, event: str, info: Any) -> None:
        """Send event async. before use MUST be added to the runloop."""
        self._pending_events.append((event, info))
        pass

    def _check(self) -> bool:
        return len(self._pending_events) > 0

    def _run(self) -> None:
        """Run for runloop running."""
        events = self._pending_events
        self._pending_events = []
        for event in events:
            self.send(event[0], event[1])
        pass

    def add_recv(self, receiver: HiEventReceiver) -> None:
        """Add a recv."""
        self._receiver_lock.run(
            lambda weakself=weakref.ref(self), recv=receiver:
            weakself()._receivers.append(recv) if weakself() is not None else None
        )
        pass

    def del_recv(self, receiver: HiEventReceiver) -> None:
        """Del a recv."""
        self._receiver_lock.run(
            lambda weakself=weakref.ref(self), recv=receiver:
            weakself()._receivers.remove(recv) if weakself() is not None else None
        )
        pass

    def del_all_recv(self) -> None:
        """Del all recv."""
        self._receiver_lock.run(
            lambda weakself=weakref.ref(self):
            weakself()._receivers.clear() if weakself() is not None else None
        )
        pass

    pass

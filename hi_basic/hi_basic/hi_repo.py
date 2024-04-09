#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 19:18:57
FilePath: /hikit/hi_basic/hi_basic/hi_repo.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 
'''

import os
from .hi_log import *
from .hi_file import *
from .hi_app import *
from .hi_tranmitter import *


class HiRepo(object):
    """For upload and download hikit package, currently using git."""

    def __init__(
            self,
            local: str = os.getcwd(),
            remote: str = "",
            transfer: HiAppTransMethod = HiAppTransMethod.GIT,
            transfer_info: dict = None) -> None:
        """Create a HiRepo.

        Args:
            local (str, optional): Where the repo locate. Defaults to os.getcwd().
            remote (str, optional): The remote address for repo. Defaults to "".
            transfer (HiAppTransMethod, optional): Transfer method. Defaults to HiAppTransMethod.GIT.
        """
        self._local = local
        self._remote = remote
        self._transfer = transfer
        # TODO: need support more transmitter.
        if transfer == HiAppTransMethod.GIT:
            self._transmitter = HiGitTransmitter(local=local, remote=remote, info=transfer_info)
            HiLog.debug("create git transmitter: " + str(local + " remote:" + str(remote) + " info:" + str(transfer_info)))
        else:
            raise ValueError(str(transfer.value) + " not support yet! ONLY support Git.")
        pass

    @classmethod
    def from_hikit(cls) -> "HiRepo":
        """Create hikit repo from current hikit."""
        return HiRepo(
            local=HiPath.libpath("hikit"),
            remote=HiPath.hikitsource
        )

    @classmethod
    def from_appinfo(cls, appinfo: HiAppInfo) -> "HiRepo":
        """Create repos from appinfo."""
        return HiRepo(
                local=HiPath.libpath(appinfo.name),
                remote=appinfo.remote
                )

    @classmethod
    def from_resources(cls, appinfo: HiAppInfo) -> list:
        """Create repos from app resources. Return type is list[HiRepo]."""
        resources = []
        for resource in appinfo.resources:
            local = HiPath.resourcepath(appinfo.name, resource.name)
            repo = HiRepo(
                local=local,
                remote=resource.url,
                transfer=resource.transfer)
            resources.append(repo)
        return resources

    @classmethod
    def from_dependencies(cls, appinfo: HiAppInfo) -> list:
        """Create repos from app dependencies. Return type is list[HiRepo]."""
        dependencies = []
        for lib in appinfo.dependencies:
            libinfo = HiAppInfo.from_source(lib)
            dependencies.append(HiRepo.from_appinfo(libinfo))
        return dependencies

    @property
    def transmitter(self) -> HiTransmitter:
        """Use to operate the repo."""
        return self._transmitter

    @property
    def exist(self) -> bool:
        """Return exist."""
        return os.path.exists(self._local)

    pass

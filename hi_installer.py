#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 15:51:03
FilePath: /hikit/hi_installer.py
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
import shutil
from hi_basic import *
from hi_basic_setup import *


class HiInstaller(object):
    """For install app. not consider copy to basic."""

    def __init__(self, appinfo: HiAppInfo) -> None:
        """Install app from app info."""
        self._info = appinfo
        self._repo = HiRepo.from_appinfo(self._info)
        pass

    @classmethod
    def make_alias(cls, name: str, alias: str) -> None:
        """Make alias for a command."""
        binpath = HiPath.binpath(name)
        aliaspath = HiPath.binpath(alias)
        if not os.path.exists(binpath):
            raise IOError(binpath + " not exist!")
        if os.path.exists(aliaspath):
            os.remove(aliaspath)
        os.symlink(binpath, aliaspath, False)
        HiLog.debug(aliaspath + " create success.")
        pass

    @classmethod
    def clean_alias(cls) -> list:
        """Cleanup all alias, return list of clean alias."""
        cmdfiles = os.listdir(HiPath.binpath())
        linkfiles = []
        for cmdfile in cmdfiles:
            filepath = HiPath.binpath(cmdfile)
            if os.path.islink(filepath):
                linkfiles.append(cmdfile)
                os.unlink(filepath)
        return linkfiles

    def conflict_commands(self) -> list:
        """Before install, should check the commands is conflict or not. Return type is list[str]."""
        conflict_list = []
        for command in self._info.commands:
            if os.path.exists(HiPath.binpath(command)):
                conflict_list.append(command)
        return conflict_list

    def install(self, include_dependency: bool = True) -> None:
        """Install a new one."""
        installed_app = HiAppInfo.from_installed(self._info.name)
        if installed_app is None:
            self._repo.transmitter.download()
        else:
            removing_commands = self._info.commands
            self._repo.transmitter.update()
            self._remove_commands(removing_commands)
        installed_app = HiAppInfo.from_installed(self._info.name)

        # Check app type to select install func.
        if installed_app.type == HiAppType.APP or installed_app.type == HiAppType.FLUTTER:
            self._build_commands(installed_app.app_path)
            self._update_requirements(installed_app.app_path)
        elif installed_app.type == HiAppType.BASIC:
            self._install_pip_module()
        else:
            raise ValueError("App Type " + str(self._info.type) + " not support yet.")

        if self._info.name == "hikit":
            install_basic()

        # download resource.
        self._download_resouces(installed_app.resources)

        # install dependencies.
        if include_dependency:
            dependency_list = []
            resolving_list = installed_app.dependencies[:]
            while len(resolving_list) > 0:
                childs_list = []
                for dependency in resolving_list:
                    # Check duplicate.
                    if dependency in dependency_list:
                        continue
                    info = HiAppInfo.from_source(dependency)
                    # Check in the source and is Basic.
                    if info is not None and info.type == HiAppType.BASIC:
                        dependency_list.append(info.name)
                        # Get sub dependencies.
                        childs_list.extend(info.dependencies)
                    pass
                # get all the childs dependencies
                resolving_list = childs_list[:]
            # install all the dependency.
            for name in dependency_list:
                installer = HiInstaller(HiAppInfo.from_source(name=name))
                installer.install(include_dependency=False)
                pass
            pass
        pass

    def uninstall(self) -> None:
        """Uninstall app."""
        if self._info.name == "hikit":
            # uninstall self.
            shutil.rmtree(HIKIT_PATH)
            return None
        self._remove_commands(commands=self._info.commands)
        if os.path.exists(HiPath.resourcepath(self._info.name)):
            shutil.rmtree(HiPath.resourcepath(self._info.name))
        if os.path.exists(HiPath.libpath(self._info.name)):
            shutil.rmtree(HiPath.libpath(self._info.name))
        pass

    def switch(self, branch: str) -> None:
        """Switch branch."""
        self._repo.transmitter.switch(branch)
        pass

    def _install_pip_module(self):
        install_pip_module(HiAppInfo.from_installed(self._info.name).app_path)
        pass

    def _build_commands(self, path: str) -> None:
        bin_template = """#!/bin/sh
# -*- coding: utf-8 -*-
<BIN_PATH> $@
"""
        for command in self._info.commands:
            source_path = os.path.join(path, command)
            bin_content = bin_template.replace("<BIN_PATH>", source_path)
            bin_path = HiPath.binpath(command)
            with open(bin_path, "w") as binfile:
                binfile.write(bin_content)
            os.chmod(bin_path, 1023)
        pass

    def _remove_commands(self, commands: list) -> None:
        for command in commands:
            bin_path = HiPath.binpath(command)
            if os.path.exists(bin_path):
                os.remove(bin_path)
        pass

    def _download_resouces(self, resources: list) -> None:
        # download resource. resources type is list[HiResourceInfo].
        for resource_info in resources:
            resource = HiResource(self._info.name, resource_info)
            if resource.exist:
                resource.transmitter.update()
            else:
                resource.transmitter.download()

    def _update_requirements(self, path: str) -> None:
        requirements_file = os.path.join(path, "requirements.txt")
        if os.path.exists(requirements_file):
            os.system(HiSys.to_bash("python3 -m pip install -r " + requirements_file))
        pass

    pass


class HiLocalInstaller(HiInstaller):
    """For install local package."""

    def install(self, include_dependency: bool = True) -> None:
        """Local install."""
        if self._info.type == HiAppType.APP or self._info.type == HiAppType.FLUTTER:
            self._update_requirements(self._info.app_path)
            self._build_commands(self._info.app_path)
            self._download_resouces(self._info.resources)
        elif self._info.type == HiAppType.BASIC:
            self._update_requirements(self._info.app_path)
            self._install_pip_module(self._info.app_path)
        else:
            raise ValueError("App Type " + str(self._info.type) + " not support yet.")
        pass

    def uninstall(self):
        """Local uninstall."""
        self._remove_commands(commands=self._info.commands)
        pass

    pass

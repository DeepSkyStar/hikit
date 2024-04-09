#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 15:50:35
FilePath: /hikit/hi_template.py
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
from hi_basic import *


class HiTemplate(object):
    """Hi Python app template.

    The template store in the template HiPath.templatepath().

    The variables in the template:

        <PROJECT_NAME> : will change to the project name.
        <PROJECT_CLASS> : will change to the project name. Follow Hump style.
    """

    def __init__(self,
                 project_name: str,
                 template_name: str):
        """For create template.

        Args:
            project_name (str): project name
            template_name (str): template name.
        """
        super().__init__()
        self._project_name = project_name.lower()
        self._template_root = []
        self._template_files = {}
        self._load_template(template_name)
        pass

    def _load_template(self, name: str):
        curdir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(curdir, "template")
        template_path = os.path.join(template_dir, name)
        if not os.path.exists(template_path):
            raise IOError("Template dir not exist, please update or reinstall the hikit!")

        # Fetch file name
        self._template_root = os.listdir(template_path)

        # Fetch the file content and replace variables.
        self._load_contents(
            template_path,
            self._template_root,
            self._template_files)
        pass

    def _load_contents(
            self,
            path: str,
            names: list,
            files: dict):
        for name in names:
            subpath = os.path.join(path, name)
            if os.path.isdir(subpath):
                subpathfiles = {}
                files[self._replace_file_name(name)] = subpathfiles
                self._load_contents(
                    subpath,
                    os.listdir(subpath),
                    subpathfiles)
            else:
                HiLog.debug("read template file:" + subpath)
                with open(subpath, "r") as tempfile:
                    content = tempfile.read()
                    content = self._replace_content(content)
                    files[self._replace_file_name(name)] = content
        pass

    def _replace_content(self, content: str) -> str:
        """Override Point."""
        return content.replace(
            "<PROJECT_NAME>", self._project_name
        ).replace(
            "<PROJECT_CLASS>",
            self._project_name.replace('_', '').capitalize()
        )

    def _replace_file_name(self, filename: str) -> str:
        return filename.replace(
                "project_name", self._project_name
                )

    def _deploy_template(self, path):
        self._deploy_files(path, self._template_root, self._template_files)
        pass

    def _deploy_files(self, path: str, files: list, contents: dict):
        for afile in files:
            afile = self._replace_file_name(afile)
            filepath = os.path.join(path, afile)
            if type(contents[afile]) == str:
                with open(filepath, "w") as deployfile:
                    deployfile.write(contents[afile])
                if afile == self._project_name:
                    os.chmod(filepath, 1023)
            elif type(contents[afile] == dict):
                os.mkdir(filepath)
                self._deploy_files(
                    filepath,
                    contents[afile].keys(),
                    contents[afile])
        pass

    def _legal_check(self, path: str, is_force: bool) -> None:
        if os.path.exists(path):
            if is_force:
                if os.path.isdir(path):
                    return None
                else:
                    raise IOError(path + " is a file.")
            else:
                raise IOError(path + " exist same name file or dir.")
        return None

    def generate_to_path(self, path: str = os.getcwd(), is_force: bool = False) -> None:
        """Generate to path."""
        path = os.path.join(path, self._project_name)
        self._legal_check(path, is_force)
        if not os.path.exists(path):
            os.mkdir(path)
        self._deploy_template(path)
        pass
    pass


class HiAppTemplate(HiTemplate):
    """Use to create normal app."""

    def __init__(self, project_name: str):
        """Init."""
        super().__init__(project_name, "app")
    pass


class HiPyModuleTemplate(HiTemplate):
    """Use to create python module."""

    def __init__(self, project_name: str):
        """Init."""
        super().__init__(project_name, "basic")
    pass


class HiSourceTemplate(HiTemplate):
    """Use to create python module."""

    def __init__(self, project_name: str):
        """Init."""
        super().__init__(project_name, "list")
    pass


class HiFlutterTemplate(HiTemplate):
    """Use to create python module."""

    def __init__(self, project_name: str):
        """Init."""
        super().__init__(project_name, "flutter")

    def generate_to_path(self, path: str = os.getcwd(), is_force: bool = False):
        """Generate file."""
        lastdir = os.getcwd()
        os.chdir(path=path)
        os.system(HiSys.to_bash("flutter create " + self._project_name))
        super().generate_to_path(path, is_force=True)
        os.chdir(lastdir)
        pass
    pass

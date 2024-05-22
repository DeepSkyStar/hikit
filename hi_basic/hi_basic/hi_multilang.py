#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-05-10 20:40:23
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-22 21:03:18
FilePath: /hikit/hi_basic/hi_basic/hi_multilang.py
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

import os
import ast
from .hi_log import *
from .hi_config import *


class HiMultiLang(object):
    """For easy multi language."""
    LANG_FILE = "multi-lang.json"
    LANG_KEY = "lang"

    def __init__(self, path: str) -> None:
        super().__init__()
        self._start_path = path
        self._langfile = HiConfig(os.path.join(path, HiMultiLang.LANG_FILE))
        pass

    @property
    def support_list(self) -> list[str]:
        """If support list is not right, will auto correct"""
        if "support" not in self._langfile:
            self._langfile.writer["support"] = ["en"]
        support = self._langfile["support"]
        if not isinstance(support, list):
            support = ["en"]
            self._langfile.writer["support"] = support
        return support

    @property
    def file_list(self) -> list[str]:
        if "text" not in self._langfile:
            self._langfile.writer["text"] = {}
            return []
        text_dict = self._langfile["text"]

        if not isinstance(text_dict, dict):
            self._langfile.writer["text"] = {}
            return []

        return list(text_dict.keys())

    def get_dict(self, filepath: str) -> dict[str, dict[str, str]]:
        file_list = self.file_list
        if filepath not in file_list:
            return {}
        if not isinstance(self._langfile["text"][filepath], dict):
            self._langfile["text"][filepath] = {}
        return self._langfile["text"][filepath]

    @property
    def start_path(self) -> str:
        return self._start_path

    def get_text(self, filepath: str, key: str) -> str:
        """If not exist key, will return key. if not exist lang, will return en."""
        lang = "en"
        if HiConfig()[HiMultiLang.LANG_KEY]:
            lang = HiConfig()[HiMultiLang.LANG_KEY]

        relpath = os.path.relpath(filepath, self.start_path)
        text_dict = self.get_dict(filepath=relpath)
        if key not in text_dict:
            return key

        if not isinstance(text_dict[key], dict):
            return key

        if lang in text_dict[key]:
            if isinstance(text_dict[key][lang], str):
                return text_dict[key][lang]
            else:
                del self._langfile.writer["text"][relpath][key][lang]
        elif "desc" in text_dict[key]:
            if isinstance(text_dict[key]["desc"], str):
                return text_dict[key]["desc"]
            else:
                self._langfile.writer["text"][relpath][key]["desc"] = key
        return key
    
    def update(self, lang_dict: dict) -> None:
        supprt = self.support_list
        cur_dict = self._langfile.items
        if "text" not in cur_dict:
            cur_dict["text"] = {}

        for file_path in lang_dict:
            if file_path not in cur_dict["text"]:
                cur_dict["text"][file_path] = {}
            text_dict = lang_dict[file_path]
            for key in text_dict:
                if key not in cur_dict["text"][file_path]:
                    cur_dict["text"][file_path][key] = {}
                    cur_dict["text"][file_path][key]["desc"] = text_dict[key]
                    cur_dict["text"][file_path][key]["en"] = text_dict[key]
                else:
                    cur_dict["text"][file_path][key]["desc"] = text_dict[key]
                pass
            pass
        self._langfile.items = cur_dict
        pass

    def add_lang(self, lang: str) -> None:
        support = self.support_list
        if lang in support:
            return None
        support.append(lang)
        self._langfile.writer["support"] = support
        return 

    @classmethod
    def find_lang_file(cls, path: str) -> str:
        return HiFile.find_first(name=HiMultiLang.LANG_FILE, path=path, is_dir=False, should_exit=False)

    @classmethod
    def generate_lang_file(cls, path: str = None) -> str:
        """Generate the lang file for project."""
        if path is None:
            path = os.getcwd()

        if not os.path.exists(path):
            raise IOError(path + " not exist!")

        if not os.path.isdir(path):
            path = os.path.dirname(path)

        lang_dict = HiMultiLang._scan_file(path, path)
        lang = HiMultiLang(path=path)
        lang.update(lang_dict)
        return path

    @staticmethod
    def _scan_file(start_dir: str, dir: str) -> dict[str, dict[str, str]]:
        lang_dict = {}
        for filename in os.listdir(dir):
            filepath = os.path.join(dir, filename)
            relpath = os.path.relpath(filepath, start_dir)
            if os.path.isdir(filepath):
                if os.path.basename(start_dir) == "hikit":
                    continue
                if filename == "template":
                    continue
                lang_dict.update(HiMultiLang._scan_file(start_dir, filepath))
            elif os.path.isfile(filepath) and filename.endswith('.py'):
                text_dict = HiMultiLang._analysis_file(filepath=filepath)
                if len(text_dict) > 0:
                    lang_dict[relpath] = text_dict
        return lang_dict

    @staticmethod
    def _analysis_file(filepath: str = None) -> dict[str, str]:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        tree = ast.parse(content)
        text_dict = {}

        # TODO: modify to general parse.
        class TextVisitor(ast.NodeVisitor):
            def visit_Call(self, node):
                if isinstance(node.func, ast.Name) and node.func.id == "HiText":
                    params = [arg.value for arg in node.args]
                    if len(params) != 2:
                        raise ValueError(filepath + " text: " + params + " format incorrect!")
                    text_dict[params[0]] = params[1]
                self.generic_visit(node)

        TextVisitor().visit(tree)
        return text_dict

    pass

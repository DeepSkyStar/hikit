#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-09 15:55:33
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-04 18:22:47
FilePath: /hikit/hi_menu_display.py
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
from hi_basic import *


class HiMenuDisplay(object):
    """For display menu."""

    WINDOW_WIDE = 100
    SPLIT_LINE = "-" * WINDOW_WIDE + "\n"
    LIST_COLUMN_FORMAT = "{:19} "

    def __init__(self) -> None:
        pass

    def pretty_list_display(self, source: HiSource = HiSource()) -> str:
        """For pretty displayed."""
        display = ""
        for group in source.group_list.groups:
            display += self._pretty_group(group=group, source=source)
            display += "\n\n"
        return display

    def _pretty_group(self, group: HiAppGroupInfo, source: HiSource = HiSource()) -> str:
        display = group.name + "\n"
        display += group.desc + "\n"
        display += "\n"
        display += self.SPLIT_LINE

        display += self.LIST_COLUMN_FORMAT.format(HiText("menu_list_name_title", "Name"))
        display += "{:40}".format(HiText("menu_list_desc_title", "Description"))
        display += self.LIST_COLUMN_FORMAT.format(HiText("menu_list_version_title", "Version"))
        display += self.LIST_COLUMN_FORMAT.format(HiText("menu_list_state_title", "State"))
        display += "\n"
        display += self.SPLIT_LINE

        for name in group.apps:
            source_info: HiAppInfo = HiAppInfo(os.path.join(source.path, name + ".json"), is_config=True)
            display += self.LIST_COLUMN_FORMAT.format(source_info.name)
            display += "{:40}".format(source_info.desc)
            display += self.LIST_COLUMN_FORMAT.format(source_info.version)

            install_info: HiAppInfo = HiAppInfo.from_installed(name=name)
            if install_info is not None:
                install_text = HiText("menu_list_install_text", "Installed") + "(" + install_info.version + ")"
                display += self.LIST_COLUMN_FORMAT.format(install_text)
            display += "\n"

        return display
    pass

#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2024-04-09 15:55:33
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-04 18:26:51
FilePath: /hikit/hi_basic/hi_basic/hi_resource.py
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

from .hi_repo import *
from .hi_app import *


class HiResource(HiRepo):
    """Resource for app provide."""

    def __init__(self, app: str, info: HiResourceInfo) -> None:
        """Init."""
        super().__init__(
            local=HiPath.resourcepath(app=app, resource=info.name),
            remote=info.url,
            transfer=info.transfer,
            transfer_info={})
        pass

    def exist(self) -> bool:
        """Check exist."""
        return os.path.exists(self._path)

    pass

#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 15:53:48
FilePath: /hikit/hi_basic/hi_basic/hi_tranmitter/hi_git_transmitter.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 
'''

from .hi_transmitter import *
from ..hi_enum import *
from ..hi_log import *
import subprocess
import os


class HiGit(object):
    def __init__(self,
                 local: str = "",
                 remote: str = "",
                 default_branch: str = "master",
                 check_status=True) -> None:
        self._name = os.path.split(local)[1]
        self._local = local
        self._remote = remote
        self._is_cloned = False
        self._head = ""
        self._default_branch = default_branch
        self._cur_branch = default_branch
        self._local_branchs = []
        self._remote_branchs = []
        if check_status:
            self.update_status()
        pass

    @classmethod
    def from_local(self, local: str = os.getcwd()) -> "HiGit":
        """Fetch git from local path."""
        return HiGit(local=local)

    def update_status(self, include_remote_branchs=False):
        """Update git status."""
        # Check is local.
        if not self._local:
            self._is_cloned = False
            return None

        # Check exist.
        if not os.path.exists(self._local):
            self._is_cloned = False
            return None

        # Check is git.
        ret_code, output = self._command("git status")
        if ret_code != 0:
            self._is_cloned = False
            return None

        # if remote is empty, try fetch remote.
        if not self._remote:
            ret_code, output = self._command("git remote get-url origin")
            if ret_code == 0:
                self._remote = output
                self._is_cloned = True
            else:
                self._is_cloned = False

        self._is_cloned = True

        # Try fetch branchs.
        ret_code, output = self._command("git branch")
        if ret_code == 0:
            lines = output.splitlines()
            branchs = []
            for line in lines:
                branch_name = line.replace(" ", "").replace("*", "")
                if line.find("*") >= 0:
                    self._cur_branch = branch_name
                branchs.append(branch_name)
        else:
            return None

        if not include_remote_branchs:
            return None

        # Try fetch remote branchs.
        ret_code, output = self._command("git branch -r")
        if ret_code == 0:
            lines = output.splitlines()
            branchs = []
            for line in lines:
                line = line.replace(" ", "").replace("*", "")
                if line.find("->") >= 0:
                    self._head = line.split("->")[-1]
                else:
                    branchs.append(line)
            self._remote_branchs = branchs
        pass

    def _exist_uncommit(self) -> bool:
        ret_code, output = self._command("git status")

        if ret_code != 0:
            raise IOError(self.local + " is not a git.")

        if output.find("nothing to commit") < 0:
            return True
        return False

    @property
    def name(self) -> str: return self._name

    @property
    def head(self) -> str: return self._head

    @property
    def remote(self) -> str: return self._remote

    @property
    def local(self) -> str: return self._local

    @property
    def is_cloned(self) -> bool: return self._is_cloned

    @property
    def cur_branch(self) -> str: return self._cur_branch

    @property
    def local_branch(self) -> list:
        """Return type is list[str]."""
        return self._local_branchs

    @property
    def remote_branch(self) -> list:
        """Return type is list[str]."""
        return self._remote_branchs

    def force_update(self, branch: str = "") -> bool:
        """Return is stash."""
        if not branch:
            branch = self._default_branch

        is_stash = False
        if self._exist_uncommit():
            ret_code, output = self._command("git add -A")
            ret_code, output = self._command("git stash save")
            is_stash = True

        # fetch update from server.
        HiLog.debug(self._local + " git fetch started!")
        ret_code, output = self._command("git fetch")
        if ret_code == 0:
            HiLog.debug(self._local + " git fetch successed!")
        else:
            error_msg = self._local + " git fetch failed, please check network and ssh key."
            HiLog.critical(error_msg)
            raise IOError(error_msg)

        # start checkout branch.
        HiLog.debug(self._local + " git checkout " + branch + " started!")
        ret_code, output = self._command("git checkout " + branch)
        if ret_code == 0:
            HiLog.debug(self._local + " git checkout " + branch + " successed!")
        else:
            error_msg = (self._local + " git checkout " + branch + " failed! Please check is the branch exist")
            HiLog.critical(error_msg)
            raise IOError(error_msg)

        # start pull to branch.
        HiLog.debug(self._local + " git pull started!")
        ret_code, output = self._command("git pull")
        if ret_code == 0:
            HiLog.debug(self._local + " git pull successed!")
        else:
            error_msg = (self._local + " git pull failed!\n" + output)
            HiLog.critical(error_msg)
            raise IOError(error_msg)

        return is_stash

    def clone(self,
              local: str = "",
              remote: str = "",
              params: str = "") -> tuple:
        """For the clone, param will cover path and origin. Return tuple[int, str]."""
        if not local:
            local = self._local
        else:
            self._local = local

        if not remote:
            remote = self._remote
        else:
            self._remote = remote

        if os.path.exists(self._local):
            HiLog.warning("Already exist " + self._local)
            return None

        HiLog.debug("local:" + str(local) + " remote:" + str(remote) + " params:" + str(params))
        clone_command = "git clone " + params + remote + " " + local
        result = self._git_command(
                        command=clone_command,
                        path=os.path.dirname(local))
        return result

    def checkout(self,
                 branch: str = "",
                 params: str = ""
                 ) -> tuple:
        """Checkout branch. Return Tuple[int, str]."""
        if not branch:
            branch = self._default_branch
        return self._command("git checkout " + params + branch)

    def commit(self,
               msg: str = "",
               params: str = ""
               ) -> tuple:
        """Commit code. Return tuple[int, str]."""
        if params:
            params = params + " "
        cmdstr = "git commit " + params + "-a -m \"" + msg + "\""
        ret_code, output = self._command(cmdstr)
        if ret_code != 0:
            HiLog.warning(output)
        return (ret_code, output)

    def push(self,
             branch: str = "",
             remote: str = "origin",
             params: str = "") -> tuple:
        """Push Code. Return tuple[int, str]."""
        cmdstr = "git push"
        if branch:
            cmdstr = "git push -u " + remote + " " + branch
        if params:
            cmdstr = cmdstr + " " + params
        ret_code, output = self._command(cmdstr)
        if ret_code != 0:
            HiLog.warning(output)
        return (ret_code, output)

    @classmethod
    def _git_command(cls, path: str, command: str) -> tuple:
        curdir = os.getcwd()
        os.chdir(path)
        # Result type is tuple[int, str]
        result = subprocess.getstatusoutput(command)
        os.chdir(curdir)
        return result

    def _command(self, command: str) -> tuple:
        # Return type is tuple[int, str]
        return self._git_command(path=self._local, command=command)

    pass


class HiGitTransferInfoKey(object):
    """Use to fetch transfer info."""

    DEFAULT_BRANCH = "default_branch"
    UPLOAD_BRANCH = "upload_branch"
    UPLOAD_MSG = "upload_msg"
    pass


class HiGitTransmitter(HiTransmitter):
    """Transfer data via Git."""

    def __init__(self, local: str, remote: str, info: dict) -> None:
        """Init git transmitter."""
        super().__init__(local, remote, info)
        if info is not None and HiGitTransferInfoKey.DEFAULT_BRANCH in info:
            self._default_branch = info[HiGitTransferInfoKey.DEFAULT_BRANCH]
        else:
            self._default_branch = "master"

        self._git = HiGit(local=self.local, remote=self.remote, default_branch=self._default_branch, check_status=False)
        pass

    def download(self) -> None:
        """Download."""
        if os.path.exists(self.local):
            raise IOError(self.local + " already exist, download failed!")
        result = self._git.clone()
        if result is None:
            HiLog.warning("Git clone failed.")
        elif result[0] != 0:
            HiLog.warning(result[1])
        pass

    def upload(self, info: str = "") -> None:
        """Upload."""
        upload_branch = info[HiGitTransferInfoKey.UPLOAD_BRANCH] if HiGitTransferInfoKey.UPLOAD_BRANCH in info else self._remote
        upload_msg = info[HiGitTransferInfoKey.UPLOAD_MSG] if HiGitTransferInfoKey.UPLOAD_MSG in info else "Update."
        is_save = self._git.force_update(branch=upload_branch)

        if is_save:
            ret_code, output = self._git._command("git stash pop")
            if ret_code != 0:
                error_msg = self._local + " stash pop failed. reason: \n" + output
                HiLog.warning(error_msg)
                raise IOError(error_msg)

            ret_code, output = self._git.commit(upload_msg)
            if ret_code != 0:
                error_msg = self._local + " commit failed. reason: \n" + output
                HiLog.warning(error_msg)
                raise IOError(error_msg)

            ret_code, output = self._git.push(branch=upload_branch)
            if ret_code != 0:
                error_msg = self._local + " push failed. reason: \n" + output
                HiLog.warning(error_msg)
                raise IOError(error_msg)
        pass

    def update(self) -> None:
        """Force update."""
        self._git.force_update(self._default_branch)
        pass

    def switch(self, version: str) -> None:
        """Switch."""
        self._git.force_update(version)
        pass

    pass

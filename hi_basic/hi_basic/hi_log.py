#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 15:52:34
FilePath: /hikit/hi_basic/hi_basic/hi_log.py
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
import sys
import json
from datetime import *
import logging


HIKIT_PATH = os.path.expanduser('~')+"/.hikit"
HIKIT_USERPATH = os.path.expanduser('~')+"/.hikit_user"
HIKIT_LOGPATH = os.path.join(HIKIT_USERPATH, "log")
HIKIT_CONFIG_NAME = "hiconfig.json"
HIKIT_LOG_LEVEL = "log_level"
_HiLog = logging.getLogger("HiLog")


class _HiLogColor(object):
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    WHITE = "\033[37m"
    DEFAULT = "\033[0m"
    pass


HiLog = _HiLog
# class HiLog(object):
#     @classmethod
#     def critical(cls, text: str):
#         _HiLog.critical(_HiLogColor.RED + text + _HiLogColor.DEFAULT)
#         pass

#     @classmethod
#     def error(cls, text: str):
#         _HiLog.error(_HiLogColor.RED + text + _HiLogColor.DEFAULT)
#         pass

#     @classmethod
#     def warning(cls, text: str):
#         _HiLog.warning(_HiLogColor.YELLOW + text + _HiLogColor.DEFAULT)
#         pass

#     @classmethod
#     def info(cls, text: str):
#         _HiLog.info(_HiLogColor.GREEN + text + _HiLogColor.DEFAULT)
#         pass
    
#     @classmethod
#     def debug(cls, text: str):
#         _HiLog.debug(_HiLogColor.BLUE + text + _HiLogColor.DEFAULT)
#         pass

#     pass


class HiLogLevel(object):
    """HiLogLevel defines."""

    CRITICAL = logging.getLevelName(logging.CRITICAL)
    ERROR = logging.getLevelName(logging.ERROR)
    WARNING = logging.getLevelName(logging.WARNING)
    INFO = logging.getLevelName(logging.INFO)
    DEBUG = logging.getLevelName(logging.DEBUG)
    pass


class HiLogFile(object):
    """When you excute a command, it will save to the log file, under ~/.hikit_user/log/ ."""

    def __init__(self, cmdname: str = ""):
        """Since a cmd execute, create a log file."""
        super().__init__()
        (path, curcmd) = os.path.split(sys.argv[0])
        (curcmd, ext) = os.path.splitext(curcmd)
        self.__cmdname = cmdname if cmdname else curcmd

        # Default will save to ~/.hikit_user/log/cmdname/
        logpath = os.path.expanduser('~')+"/.hikit_user"
        if not os.path.exists(logpath):
            os.mkdir(logpath)
        elif not os.path.isdir(logpath):
            print(logpath + "should not be a file!")
            raise IOError(logpath + "should not be a file!")

        logpath = os.path.join(logpath, "log")
        if not os.path.exists(logpath):
            os.mkdir(logpath)
        elif not os.path.isdir(logpath):
            print(logpath + "should not be a file!")
            raise IOError(logpath + "should not be a file!")

        logpath = os.path.join(logpath, "uname" if not self.__cmdname else self.__cmdname)
        if not os.path.exists(logpath):
            os.mkdir(logpath)
        elif not os.path.isdir(logpath):
            print(logpath + "should not be a file!")
            raise IOError(logpath + "should not be a file!")

        self.__dir = logpath
        self.__createdate = datetime.now()

        dateformatter = "%Y-%m-%d_%H-%M-%S_%f"

        if cmdname:
            loglist: list = os.listdir(self.__dir)
            loglist.sort()
            self.__path = os.path.join(self.__dir, loglist[-1])
            (name, ext) = os.path.splitext(loglist[-1])
            self.__createdate = datetime.strptime(name, dateformatter)
        else:
            name = self.__createdate.strftime(dateformatter) + ".log"
            self.__path = os.path.join(self.__dir, name)
        pass

    @property
    def dir(self) -> str:
        return self.__dir

    @property
    def path(self) -> str:
        return self.__path

    @property
    def cmdname(self) -> str:
        return self.__cmdname

    @property
    def createdate(self) -> str:
        return self.__createdate

    @classmethod
    def _get_log_level(cls) -> int:
        config_path = os.path.join(HIKIT_PATH, HIKIT_CONFIG_NAME)
        if not os.path.exists(config_path) or not os.path.isfile(config_path):
            return logging.INFO

        result = logging.INFO
        with open(config_path, "r") as jsonfile:
            try:
                items = json.load(jsonfile)
                if HIKIT_LOG_LEVEL in items:
                    text = items[HIKIT_LOG_LEVEL]
                    if text == HiLogLevel.CRITICAL:
                        result = logging.CRITICAL
                    elif text == HiLogLevel.ERROR:
                        result = logging.ERROR
                    elif text == HiLogLevel.INFO:
                        result = logging.INFO
                    elif text == HiLogLevel.DEBUG:
                        result = logging.DEBUG
                    else:
                        result = logging.INFO
                else:
                    result = logging.INFO
            except ValueError:
                result = logging.INFO
        return result

    pass


def __hilog_init(logger: logging.Logger):
    # setup the log leval
    logger.setLevel(logging.DEBUG)

    # console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(HiLogFile._get_log_level())

    # file Handler
    # !!!Here HARDCODE the userpath.
    logpath = HIKIT_USERPATH
    if not os.path.exists(logpath):
        os.mkdir(logpath)

    logpath = os.path.join(logpath, "log")
    if not os.path.exists(logpath):
        os.mkdir(logpath)

    if not os.path.exists(logpath):
        os.mkdir(logpath)

    logfile = HiLogFile()
    file_handler = logging.FileHandler(
        logfile.path,
        mode='w',
        encoding='UTF-8')
    file_handler.setLevel(logging.NOTSET)

    # formatter
    file_format = "%(asctime)s %(filename)s:%(lineno)d %(funcName)s [%(levelname)s] %(message)s"
    console_format = file_format
    if HiLogFile._get_log_level() >= logging.INFO:
        console_format = "%(asctime)s [%(levelname)s] %(message)s"

    file_handler.setFormatter(logging.Formatter(file_format))
    console_handler.setFormatter(logging.Formatter(console_format))

    # add to the Logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # print the argv in first line
    logger.debug("start:" + str(sys.argv))
    pass


__hilog_init(_HiLog)

#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-05-08 19:47:48
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 15:52:24
FilePath: /hikit/hi_basic/hi_basic/hi_regex.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 
'''

import re


class HiCharSet(object):
    """For Create Charater Set.

    Example like:

    set = HiCharSet().from_to("a","z").from_to("A","Z").set()

    Can create a charater set like [a-zA-Z].
    """

    def __init__(self, chars: str = "") -> None:
        """Create a charater set, PLEASE DO NOT include "[" and "]"."""
        self.__chars = chars
        pass

    def from_to(self, start: str, end: str) -> "HiCharSet":
        """Add a charater range into set."""
        if len(start) == 1 and len(end) == 1:
            self.__chars = self.__chars + start + "-" + end
        return self

    def add(self, chars: str) -> "HiCharSet":
        """Add more charaters into set."""
        self.__chars = self.__chars + chars
        return self

    def set(self) -> str:
        """Return a regex string for this charater set."""
        return "[" + self.__chars + "]"

    def other_set(self) -> str:
        """Return a regex string for charater set exclusive this."""
        return "[^" + self.__chars + "]"

    @classmethod
    def all_num_chars(cls) -> "HiCharSet": return HiCharSet(r"\w")

    @classmethod
    def all_non_num_chars(cls) -> "HiCharSet": return HiCharSet(r"\W")

    @classmethod
    def all_num(cls) -> "HiCharSet": return HiCharSet(r"\d")

    @classmethod
    def all_non_num(cls) -> "HiCharSet": return HiCharSet(r"\D")

    @classmethod
    def all_chars_space(cls) -> "HiCharSet": return HiCharSet(r"\s")

    @classmethod
    def all_non_chars_space(cls) -> "HiCharSet": return HiCharSet(r"\S")

    pass


class HiRegex(object):
    """For easy write and read regex string.

    Example,

    regex = HiRegex("the.").repeat(0, 1) + HiRegex("cat")

    pattern = regex.compile()

    pattern.match("The cat looks like a super cat.")

    or:

    re.match(regex.pattern, "The cat looks like a super cat.")
    """

    def __init__(self, pattern: str) -> None:
        r"""Pattern for Basic Matchers.

        You can fill up some "." to indicates that there is one character.

        And also can create Character Sets from HiCharSet.

        If include "{ } [ ] / \ + * . $ ^ | ?", should use escape character \.
        """
        super().__init__()
        self.__regex = pattern
        pass

    @property
    def pattern(self) -> str:
        """Return pattern string of this regex."""
        return self.__regex

    def compile(
        self,
        flags: re.RegexFlag = 0,
            ) -> re.Pattern:
        """Output the final regex compile."""
        return re.compile(self.pattern, flags=flags)

    def __add__(self, rhs: "HiRegex") -> "HiRegex":
        """Return a new HiRegex which connect two regex with bracket."""
        return HiRegex("(" + self.pattern + ")" + "(" + rhs.pattern + ")")

    def __or__(self, rhs: "HiRegex") -> "HiRegex":
        """Return a new HiRegex which connect two regex with |."""
        return HiRegex("(" + self.pattern + ")" + "|" + "(" + rhs.pattern + ")")

    def match_first(self) -> "HiRegex":
        """Must match the first charater in one line."""
        return HiRegex("^" + self.pattern)

    def match_last(self) -> "HiRegex":
        """Must match last charater in one line."""
        return HiRegex(self.pattern + "$")

    def non_capturing(self) -> "HiRegex":
        """Match any except this."""
        return HiRegex("(?:" + self.pattern + ")")

    def repeat(self, start: int = -1, end: int = -1, lazy_match=False) -> "HiRegex":
        """Must repeat this pattern for a count range. Default is greed match."""
        if start < 0 and end < 0:
            raise ValueError("Cannot repeat start from -1 to -1.")
        if start >= 0 and end >= 0 and start > end:
            raise ValueError("The end must be bigger or equal then start.")
        repeat_pattern = "{" + str(start) if start >= 0 else "" + "," + str(end) if end >= 0 else "" + "}"
        return HiRegex(self.pattern + repeat_pattern + "?" if lazy_match else "")

    def before_match(self, regex: "HiRegex", is_true=True) -> "HiRegex":
        """Must match another regex which behind this at first. Default need it's true."""
        if is_true:
            return HiRegex("(" + self.pattern + ")" + "(?=" + regex.pattern + ")")
        else:
            return HiRegex("(" + self.pattern + ")" + "(?!" + regex.pattern + ")")

    def behind_match(self, regex: "HiRegex", is_true=True) -> "HiRegex":
        """Must match another regex which before this at first. Default need it's true."""
        if is_true:
            return HiRegex("(?<=" + regex.pattern + ")" + "(" + self.pattern + ")")
        else:
            return HiRegex("(?<!" + regex.pattern + ")" + "(" + self.pattern + ")")

    pass

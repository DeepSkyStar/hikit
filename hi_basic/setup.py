#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hi_basic",
    version="1.0.0",
    author="Hyper Visual",
    author_email="hypervisual@hotmail.com",
    description="Hi Basic 基础库",
    long_description=long_description,
    # url="git@deepskystar.com:eva/eva.git",
    packages=setuptools.find_packages(),
    test_suite="hi_basic.tests.test_all",
    install_requires=[],
    entry_points={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License",
        "Operating System :: OS Independent",
    ],
)
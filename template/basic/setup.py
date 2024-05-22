#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="<PROJECT_NAME>",
    version="1.0.0",
    author="",
    author_email="",
    description="<PROJECT_NAME>",
    long_description=long_description,
    url="",
    packages=setuptools.find_packages(),
    test_suite="<PROJECT_NAME>.tests.test_all",
    install_requires=[],
    entry_points={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
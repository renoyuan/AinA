#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA setup
# CREATE_TIME: 2024/7/24 17:12
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note:
import setuptools
from aina import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reno_aina",
    version=__version__,
    author="renoyuan",
    author_email="renoyuan@foxmail.com",
    description="reno aina",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/renoyuan/AinA",
    packages=setuptools.find_packages(exclude=["README.md", ".vscode", ".vscode.*", ".git", ".git.*","doc","assets","test","gui"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],

    install_requires=[  ### 依赖包
        "fastapi>=0.111.1",
        "loguru>=0.7.2",
        "qianfan>=0.4.2",
        "torch>=2.3.1",
        "transformers>=4.42.4",
        "gradio>=4.39.0"
    ],
    python_requires='>=3.11',
)
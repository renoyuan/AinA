#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA __init__.py
# CREATE_TIME: 2024/7/22 16:30
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note: call model
import tomllib

from .model import ModelBase, HTTPModelBase, QWenModelBase

with open('config.toml', 'rb') as f:
    config = tomllib.load(f)
llm_model = None

# 访问配置
if config["use_model"] == 'qwen':
    print("init qwen model")
    model_path = config['qwen']['model_path']
    llm_model = QWenModelBase(model_path=model_path)


def get_model():
    return llm_model


ALL = ["ModelBase", "HTTPModelBase", "QWenModelBase", "get_model"]

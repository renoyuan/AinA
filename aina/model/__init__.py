#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA __init__.py
# CREATE_TIME: 2024/7/22 16:30
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note: call model
import os
import tomllib

from .model import ModelBase, HTTPModelBase, QWenModel, QianFanModel
from .msg import Msg

with open('config.toml', 'rb') as f:
    config = tomllib.load(f)
llm_model = None
LLM_MAP = {}
msg = Msg()
use_model = config["use_model"]
class LLMModel(object):
    def __init__(self):
        for i in use_model:
            if i == 'qwen':
                print("init qwen model")
                model_path = config['qwen']['model_path']
                LLM_MAP['qwen'] = QWenModel(model_path=model_path, msg=msg)
            elif i == 'qianfan':
                print("init qwen model")
                os.environ["QIANFAN_ACCESS_KEY"] = config["qianfan"]["access_key"]
                os.environ["QIANFAN_SECRET_KEY"] = config["qianfan"]["secret_key"]
                model_name = config["qianfan"]["model_name"]
                LLM_MAP['qianfan'] = QianFanModel(model_name=model_name, msg=msg)
    def get_model(self,key="qwen"):
        return LLM_MAP[key]
    def get_use_model(self):
        return use_model

llmModel = LLMModel()
def get_msg():
    return msg


ALL = ["ModelBase", "HTTPModelBase", "QWenModelBase", "get_model", "llmModel"]

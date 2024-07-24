#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA call_qianfan
# CREATE_TIME: 2024/7/24 10:22
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note:

import os
import tomllib

import qianfan

with open('../config.toml', 'rb') as f:
    config = tomllib.load(f)
# 动态获取最新模型列表依赖 IAM Access Key 进行鉴权，使用应用 AK 鉴权时不支持该功能
os.environ["QIANFAN_ACCESS_KEY"] = config["qianfan"]["access_key"]
os.environ["QIANFAN_SECRET_KEY"] = config["qianfan"]["secret_key"]
qianfan_model = qianfan.ChatCompletion.models()
print(qianfan_model, len(qianfan_model))
# 模型名称可以通过 qianfan.ChatCompletion.models() 获取
# 也可以在命令行运行 qianfan chat --list-model 查看
chat_comp = qianfan.ChatCompletion(model="ERNIE-Speed-128K")
# chat_comp = qianfan.ChatCompletion(model="ERNIE-Tiny-8K")
# chat_comp = qianfan.ChatCompletion(model="ERNIE-4.0-Turbo-8K")
# chat_comp = qianfan.ChatCompletion(model="ERNIE-Speed-128K")
resp = chat_comp.do(
    messages=[
        {"role": "user", "content": "你好，千帆"},
        # {"role": "assistant", "content": "你好，千帆"},
        # {"role": "user", "content": "你好,不要重复我说的话"},
              ],
    # （可选）设置模型参数，与 API 参数一致
    top_p=0.8,
    temperature=0.9,
    penalty_score=1.0,
)

print(resp.get("result"))
# print(resp)

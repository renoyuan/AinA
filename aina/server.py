#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA server
# CREATE_TIME: 2024/7/22 16:28
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note: server
import tomllib
from pydantic import BaseModel

from loguru import logger
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import Optional,List,Union

from model import QWenModelBase

# 创建 FastAPI 应用实例
app = FastAPI()

with open('config.toml', 'rb') as f:
    config = tomllib.load(f)
llm_model = None

# 访问配置
if config["use_model"] == 'qwen':
    print("init qwen model")
    model_path = config['qwen']['model_path']
    llm_model = QWenModelBase(model_path=model_path)

class Item(BaseModel):
    query: str

@app.post("/llm_chat")
def llm_chat(query: Optional[str]=None,item:Item=None):
    headers = {
        'Transfer-Encoding': 'chunked',
        'Connection': 'close',
    }

    query = item.query
    # print(query)
    answer = llm_model.predict(query=query)
    return answer




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)

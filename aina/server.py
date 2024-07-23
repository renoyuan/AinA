#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA server
# CREATE_TIME: 2024/7/22 16:28
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note: server

from fastapi import FastAPI

# 创建 FastAPI 应用实例
app = FastAPI()

from api import api_router

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)

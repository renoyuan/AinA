#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA server
# CREATE_TIME: 2024/7/22 16:28
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note: server
import tomllib

from flask import Flask,request
# 访问配置
app = Flask(__name__)

@app.route("/llm_chat", methods=['POST'])
def llm_chat( ):


    return "a"




if __name__ == "__main__":
    app.run("0.0.0.0",8000,debug=True)

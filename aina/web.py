#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA web
# CREATE_TIME: 2024/7/24 16:45
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note:
import random
import uuid

import gradio as gr
import requests

session_id = str(uuid.uuid4())
url = "http://192.168.1.6:8001/api/llm_chat"
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])


    def respond(message, chat_history):
        res = requests.post(url=url, json={
            "query": message,
            "session_id": session_id
        })
        answer = res.json()["data"]["answer"]
        chat_history.append((message, answer))

        return "", chat_history


    msg.submit(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch()

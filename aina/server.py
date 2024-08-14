#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA server
# CREATE_TIME: 2024/7/22 16:28
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note: server

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8001/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
# 创建 FastAPI 应用实例
app = FastAPI()

from api import api_router

app.include_router(api_router)
origins=["*","http://localhost:5174/"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()

        await websocket.send_text(f"Message text was: {data}")
        if data == "close":
            await websocket.send_text(f"Message connection was: {data}")
            await websocket.close(1000, "Closing the connection.")

if __name__ == "__main__":
    import uvicorn

    text = "aina"
    from transe_logo import Transform
    print(Transform.transform(text))
    uvicorn.run(app, host="0.0.0.0", port=8001)

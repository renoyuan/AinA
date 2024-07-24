#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA api.py
# CREATE_TIME: 2024/7/23 16:20
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note:
import os
import sys
import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from loguru import logger
from pydantic import BaseModel

from .response import gen_response

api_router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


class Item(BaseModel):
    query: Optional[str] = None
    session_id: Optional[str] = None


# get_model=None

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
print(sys.path)

from aina.model import get_model, get_msg

@api_router.post("/del_session")
def del_session(item: Item = None, msg=Depends(get_msg)):
    session_id = item.session_id
    if not session_id:
        return gen_response(602)
    msg.del_session(session_id)
    return gen_response()

@api_router.post("/llm_chat")
def llm_chat(item: Item = None, llm_model=Depends(get_model)):
    logger.info(f"{item}")
    query = item.query
    session_id = item.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
    answer = llm_model.predict(session_id=session_id, query=query)

    return gen_response(data={
        "answer": answer,
        "session_id": session_id

    })

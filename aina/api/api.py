#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA api.py
# CREATE_TIME: 2024/7/23 16:20
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note:
import os
import sys

from fastapi import APIRouter, Depends
from pydantic import BaseModel

api_router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


class Item(BaseModel):
    query: str


# get_model=None

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
print(sys.path)

from aina.model import get_model


@api_router.post("/llm_chat")
def llm_chat(item: Item = None, llm_model=Depends(get_model)):
    headers = {
        'Transfer-Encoding': 'chunked',
        'Connection': 'close',
    }

    query = item.query
    # print(query)

    answer = llm_model.predict(query=query)
    return answer

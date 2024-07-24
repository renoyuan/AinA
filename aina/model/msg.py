#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA msg
# CREATE_TIME: 2024/7/24 15:02
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note: 存储历史信息

from loguru import logger


class Msg(object):
    _instance = None

    def __init__(self, *args, **kwargs):
        self.session = {}

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def get_session(self, session_id: str) -> list:
        if session_id in self.session:
            return self.session[session_id]
        else:
            return []

    def del_session(self, session_id):
        self.session.pop(session_id, None)
        logger.info(f"del_session{session_id}")

    def put_session(self, session_id, msg: list):
        self.session[session_id] = msg

    def new_session(self, session_id):
        self.session[session_id] = []

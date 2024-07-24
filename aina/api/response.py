#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA response
# CREATE_TIME: 2024/7/24 14:53
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note:

code_map = {
    200: ("操作成功", 1),
    601: ("操作失败！", 0),
    401: ("token验证失败！", 0),
    602: ("非法参数！", 0),
    603: ("必要参数不能为空", 0),
    604: ("此操作需要登陆系统！", 0),
    605: ("权限不足，无权操作！", 0),
    606: ("新增失败", 0),
    607: ("删除失败", 0),
    608: ("修改失败", 0),
    609: ("该记录关键字段已经存在", 0),
    610: ("id不能为空", 0),
    611: ("无查询结果!！", 0),
    612: ("找到路径！", 0),
    613: ("当前用户无操作权限！", 0),
    614: ("仅支持pdf文件拆分，请检查文件类型！", 0),
    615: ("TaskSn不合法", 0),
    616: ("任务等待中", 0),
    617: ("任务失败", 0),
    618: ("fastdfs错误", 0),
    619: ("场景不存在", 0),

}


def gen_response(code=200, data=None) -> dict:
    response = {"code": str(code), "message": str(code_map[code][0]), "status": str(code_map[code][1]), "data": data}
    return response


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA search
# CREATE_TIME: 2024/7/25 9:47
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note: pip install selenium webdriver_manager requests

from abc import abstractmethod


class SearchBase(object):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def search(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")


class BaiduSearch(SearchBase):
    def __init__(self,):
        "POST"
        """
        参数名	类型	是否必填	说明
        Content-Type	-	是	application/json;charset=UTF-8
        X-Gw-Ak	string	是	推荐服务鉴权信息
        Alias-Name	string	是	推荐服务应用名
        """
        url = "http://airec.baidu.com/airec/api/search/main"


class BingSearch(SearchBase):
    pass


class GoogleSearch(SearchBase):
    pass

import requests

def google_custom_search(query, api_key, cse_id, **kwargs):
    service_url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
    }
    params.update(kwargs)  # 更新额外的参数，例如num=10来获取10个结果
    response = requests.get(service_url, params=params)
    return response.json()

# 替换以下值为你自己的API密钥和CX值
api_key = "YOUR_API_KEY"
cse_id = "YOUR_CSE_ID"

# 调用函数
results = google_custom_search(
    '智能体',
    api_key=api_key,
    cse_id=cse_id,
    num=10  # 可选参数，指定返回的结果数量
)

# 打印结果
for item in results['items']:
    print(item['title'])
    print(item['link'])
    print('-' * 50)
# 运行函数
if __name__ == "__main__":
    pass

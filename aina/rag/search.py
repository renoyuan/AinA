#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA search
# CREATE_TIME: 2024/7/25 9:47
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note: pip install selenium webdriver_manager requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time


def bing_search(query):
    try:
        # 构造搜索 URL
        url = f"https://www.bing.com/search?form=QBRE&q={requests.utils.quote(query)}&cc=US"

        # 启动 Chrome 浏览器
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        # 访问页面
        driver.get(url)

        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "b_results"))
        )

        # 获取搜索结果
        results = driver.find_elements(By.CSS_SELECTOR, "#b_results .b_algo")

        summaries = []
        for result in results[:5]:  # 只获取前五个结果
            try:
                abstract_element = result.find_element(By.CSS_SELECTOR, ".b_caption > p")
                link_element = result.find_element(By.TAG_NAME, "a")
                href = link_element.get_attribute("href")
                title = link_element.text

                abstract = abstract_element.text if abstract_element else ""

                summaries.append({"href": href, "title": title, "abstract": abstract})
            except Exception as e:
                print(f"Error processing result: {e}")

        # 关闭浏览器
        driver.quit()

        print(summaries)
        return summaries

    except Exception as error:
        print("An error occurred:", error)


# 运行函数
if __name__ == "__main__":
    bing_search("特朗普")

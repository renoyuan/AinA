# AINA IS ALL IN AL

目前定位可能是一个大模型使用 工具 。

## 目前已实现

当前版本 v0.1.0

调用大模型 ok

    调用qwen2 大模型（本地）
    
    调用文心一言（千帆大模型）（在线）文心一言 没有开源只能调用线上版本目前有免费次数可用去官网申请即可



多轮对话+展示页面 ok

本地文档 文件名不能包含中文和特殊符号




## 启动

### 安装依赖

python 版本

    3.12.4

安装依赖

```
python -m pip install -r requirments.txt
```



### 启动服务

```
cd aina

# 启动后台服务
python server.py

# 启动 展示页面
python we.py
```



## 版本规划

v0.0.1  运行模型(支持多模型) 输入&回答

v0.1.0   多轮对话 +展示页面

v1.0.0  引入 rag 本地文档+搜索引擎

v1.1.0  多功能 模板

v1.2.0  多模态支持

v1.3.0  支持多平台接入

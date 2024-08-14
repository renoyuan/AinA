#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA a
# CREATE_TIME: 2024/7/25 11:00
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note: 对小说类的效果不好
import os
import time

import faiss
import nltk
import numpy as np
import torch
from faiss import IndexFlatIP
from loguru import logger
from transformers import AutoTokenizer, AutoModel

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'


class SplitText(object):
    def split_line(self, text):
        """text"""
        segments = text.split("\n")
        return segments

    def split_sentence(self, text):
        """sentence"""
        sentences = nltk.sent_tokenize(text)
        return sentences

    def sliding_window(self, text, window_size=3, stride=1):
        """滑动窗口方法"""
        sentences = nltk.sent_tokenize(text)
        segments = []
        start = 0
        while start + window_size <= len(sentences):
            segment = " ".join(sentences[start:start + window_size])
            segments.append(segment)
            start += stride
        return segments
    def sliding_window_line(self, text, window_size=3, stride=1):
        sentences = text.split("\n")
        segments = []
        start = 0
        while start + window_size <= len(sentences):
            segment = " ".join(sentences[start:start + window_size])
            segments.append(segment)
            start += stride
        return segments
    def split_by_length(self, text, max_length=20):
        """# 基于长度的分割"""
        tokens = nltk.word_tokenize(text)
        segments = []
        current_segment = []
        current_length = 0
        for token in tokens:
            if current_length + len(token) > max_length:
                segments.append(" ".join(current_segment))
                current_segment = [token]
                current_length = len(token)
            else:
                current_segment.append(token)
                current_length += len(token)
        if current_segment:
            segments.append(" ".join(current_segment))
        return segments

    def __call__(self, text, mode="sliding_window_line") -> list:
        segments = []
        if mode == "split_line":
            segments = self.split_line(text)
        if mode == "split_sentence":
            segments = self.split_sentence(text)
        if mode == "sliding_window":
            segments = self.sliding_window(text)
        if mode == "sliding_window_line":
            segments = self.sliding_window_line(text)
        if mode == "split_by_length":
            segments = self.split_by_length(text)
        return segments


class VectorDoc(object):
    _instance = None

    def __init__(self, *args, **kwargs):

        self.vector_text_map = {}
        self.index_dir_path = kwargs.get("index_dir_path")

        self.spliter = SplitText()
        model_path = kwargs.get("model_path")

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def encode_text(self, text):
        """encode_text"""
        print("encode_text", text)
        encoded_inputs = self.tokenizer(text, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            model_output = self.model(**encoded_inputs)
        embeddings = model_output.last_hidden_state[:, 0, :]
        return embeddings.numpy()

    def save_index(self, index, doc_id):
        # 保存索引到文件
        name = f"{doc_id}.faiss"
        path = os.path.join(self.index_dir_path, name)
        # path = os.fsencode(path)
        faiss.write_index(index, path)

    def load_index(self, doc_id):
        # 加载索引
        name = f"{doc_id}.faiss"
        path = os.path.join(self.index_dir_path, name)
        # path = os.fsencode(path)
        if os.path.exists(path):
            index = faiss.read_index(path)
            return index

    def create_index(self, doc_id, text):
        t1 = time.time()

        index = self.load_index(doc_id)

        if doc_id in self.vector_text_map:
            print("doc_id existed")
            return
        segments = self.spliter(text)
        if not segments:
            print(" segments is NULL")
            return
        self.vector_text_map[doc_id] = {
            "index": index,
            "segments": segments
        }

        if index:
            return index

        for seg in segments:
            embeddings = self.encode_text(seg)
            if index is None:
                index = IndexFlatIP(embeddings.shape[1])
            index.add(embeddings)

        self.vector_text_map[doc_id]["index"] = index
        logger.info(f"create_index coat {time.time() - t1}")
        self.save_index(index,doc_id)
    def get_text(self, doc_id, text, ):
        t1 = time.time()
        if doc_id not in self.vector_text_map:
            print("")
            return
        query_embedding = self.encode_text([text])[0]
        # print(self.vector_text_map)
        index = self.vector_text_map[doc_id]["index"]
        # 检索
        top_k = 3
        D, I = index.search(np.array([query_embedding]), top_k)
        print(D, I)
        for i in I[0]:
            self.vector_text_map[doc_id]["segments"][i]
            print(self.vector_text_map[doc_id]["segments"][i])

        logger.info(f"get_text coat {time.time() - t1}")


if __name__ == "__main__":
    doc_path = r"F:\llm\AinA\assets\aaa.txt"
    with open(doc_path, "r", encoding="gbk") as f:
        text = f.read()
    model_path = r"F:\llm\AinA\assets\bert"
    index_dir_path = r"F:\llm\AinA\assets\index"
    v_d = VectorDoc(model_path=model_path, index_dir_path=index_dir_path)  # model_path=r"F:\llm\AinA\assets\bert"
    v_d.create_index("aaa", text)
    v_d.get_text("aaa", "最后结局是什么？")

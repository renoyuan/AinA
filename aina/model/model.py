#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA model.py
# CREATE_TIME: 2024/7/22 18:52
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note:
import argparse
import os
import platform
import shutil
from abc import abstractmethod
from copy import deepcopy
from threading import Thread


class ModelBase(object):

    def __init__(self, *args, **kwargs):
        """create predictor"""
        self.msg = kwargs["msg"]

    def add_history(self, session_id, role, text):
        session = self.msg.get_session(session_id)
        msg = {"role": role,
               "content": text}
        session.append(msg)
        self.msg.put_session(session_id,session)

    @abstractmethod
    def predict(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def predict_stream(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")


class LocalModel(ModelBase):
    pass


class QWenModel(LocalModel):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """create predictor"""
        super.__init__(*args, **kwargs)
        print("create qwen predictor")
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
        from transformers.trainer_utils import set_seed
        self.torch = torch
        self.AutoModelForCausalLM = AutoModelForCausalLM
        self.AutoTokenizer = AutoTokenizer
        self.TextIteratorStreamer = TextIteratorStreamer
        self.set_seed = set_seed

        model_path = kwargs.get("model_path")
        parser = argparse.ArgumentParser(description='QWen2')
        parser.add_argument("-c", "--checkpoint-path", type=str, default=model_path,
                            help="Checkpoint name or path, default to %(default)r")
        parser.add_argument("-s", "--seed", type=int, default=1234, help="Random seed")
        parser.add_argument("--cpu-only", action="store_true", help="Run demo with CPU only")
        self.model_args = parser.parse_args()

        self.seed = self.model_args.seed
        history, response = [], ''
        self.history = history

        model, tokenizer = self._load_model_tokenizer(self.model_args)
        self.model = model
        self.tokenizer = tokenizer
        orig_gen_config = deepcopy(model.generation_config)

    def _load_model_tokenizer(self, args):
        tokenizer = self.AutoTokenizer.from_pretrained(
            args.checkpoint_path, resume_download=True,
        )

        if args.cpu_only:
            device_map = "cpu"
        else:
            device_map = "auto"

        model = self.AutoModelForCausalLM.from_pretrained(
            args.checkpoint_path,
            torch_dtype="auto",
            device_map=device_map,
            resume_download=True,
        ).eval()
        model.generation_config.max_new_tokens = 2048  # For chat.

        return model, tokenizer

    def _gc(self, ):
        import gc
        gc.collect()
        if self.torch.cuda.is_available():
            self.torch.cuda.empty_cache()

    def _clear_screen(self, ):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def _print_history(self, history):
        terminal_width = shutil.get_terminal_size()[0]
        print(f'History ({len(history)})'.center(terminal_width, '='))
        for index, (query, response) in enumerate(history):
            print(f'User[{index}]: {query}')
            print(f'QWen[{index}]: {response}')
        print('=' * terminal_width)

    def _chat_stream(self, model, tokenizer, query, history):

        conversation = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
        ]
        for query_h, response_h in history:
            conversation.append({'role': 'user', 'content': query_h})
            conversation.append({'role': 'assistant', 'content': response_h})
        conversation.append({'role': 'user', 'content': query})
        inputs = tokenizer.apply_chat_template(
            conversation,
            add_generation_prompt=True,
            return_tensors='pt',
        )
        inputs = inputs.to(model.device)
        streamer = self.TextIteratorStreamer(tokenizer=tokenizer, skip_prompt=True, timeout=60.0,
                                             skip_special_tokens=True)
        generation_kwargs = dict(
            input_ids=inputs,
            streamer=streamer,
        )
        thread = Thread(target=model.generate, kwargs=generation_kwargs)
        thread.start()

        for new_text in streamer:
            yield new_text

    def predict_stream(self):
        pass

    def predict(self, *args, **kwargs):

        # Run chat.
        self.set_seed(self.seed)

        model = self.model
        tokenizer = self.tokenizer
        query = kwargs.get("query")
        history = self.history

        partial_text = ''
        for new_text in self._chat_stream(model, tokenizer, query, history):
            print(new_text, end='', flush=True)
            partial_text += new_text
        response = partial_text
        print(response)

        history.append((query, response))
        return response


class HTTPModelBase(ModelBase):
    pass


class QianFanModel(HTTPModelBase):
    def __init__(self, *args, **kwargs):
        super().__init__(QianFanModel, *args, **kwargs)
        import qianfan
        self.qianfan = qianfan
        self.history = []  # 這個後續要改造
        model_name = kwargs.get("model_name", "ERNIE-3.5-8K")

        # 也可以在命令行运行 qianfan chat --list-model 查看
        self.chat_comp = self.qianfan.ChatCompletion(model=model_name)

    def predict(self, *args, **kwargs):
        query = kwargs.get("query")
        session_id = kwargs.get("session_id")

        self.add_history(session_id, "user", query)
        msg = self.msg.get_session(session_id)
        print(msg)
        resp = self.chat_comp.do(
            messages=msg,
            # （可选）设置模型参数，与 API 参数一致
            top_p=0.8,
            temperature=0.9,
            penalty_score=1.0,
        )

        resp_text = resp.get("result", "")
        self.add_history(session_id, "assistant", resp_text)
        return resp_text

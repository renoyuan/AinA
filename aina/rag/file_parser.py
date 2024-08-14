#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROJECT_NAME: AinA file_parser
# CREATE_TIME: 2024/7/24 17:57
# E_MAIL: renoyuan@foxmail.com
# AUTHOR: renoyuan
# note: 文档解析
import fitz

class FileParserBase(object):
    """file2textBase"""
    def read(self):
        pass
    def format(self,page_list):
        text = ""
        for idx, page in enumerate(page_list):
            for line in page:
                text += line
            text += f"\npage{idx}\n"
        return text



class PDFParserParser(FileParserBase):
    pass


class DocxParserParser(FileParserBase):
    pass

class XlsxParserParser(FileParserBase):
    pass


class ParserFile(object):
    def __init__(self):
        self.pfd_parser = PDFParserParser()
        self.docx_parser = DocxParserParser()
        self.xlsx_parser = XlsxParserParser()
    def __call__(self,file_type):
        if file_type in ["pfd"]:
            return  self.pfd_parser()
        elif file_type in ["docx"]:
            return self.docx_parser()
        elif file_type in ["Xlsx"]:
            return self.xlsx_parser()


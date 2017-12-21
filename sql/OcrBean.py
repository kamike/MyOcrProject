#!/usr/bin/env python
# -*- coding:utf8 -*-

import datetime


class OcrBean:
    def __init__(self, content, file_id, key_word, type, search_url):
        self.content = content
        self.file_id = file_id
        self.key_word = key_word
        self.type = type
        self.search_url = search_url
        self.search_url = search_url
        self.create_date = datetime.datetime.now()

    def __getParaStr__(self) -> str:
        return "content,file_id,key_word,type,search_url,create_date"

    def __str__(self) -> str:
        return "'"+self.content + "'," + str(self.file_id) + ",'" + self.key_word + "','" + self.type + "','" + self.search_url + "','" + str(self.create_date)+"'"

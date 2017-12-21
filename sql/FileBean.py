#!/usr/bin/env python
# -*- coding:utf8 -*-

import datetime


class FileBean:
    def __init__(self, url, name, local_path, size, md5, width, height, type):
        self.url = url
        self.name = name
        self.local_path = local_path
        self.size = size
        self.md5 = md5
        self.width = width
        self.height = height
        self.type = type
        self.create_date = datetime.datetime.now()

    def __getParaStr__(self) -> str:
        return "url,name,local_path,size,md5,width,height,type,create_date"

    def __str__(self) -> str:
        return "'"+self.url + "','" + self.name + "','" + self.local_path + "'," + self.size + ",'" + self.md5 + "','" + self.width + "','" + self.height + "','" + self.type + "','" + str(self.create_date)+"'"
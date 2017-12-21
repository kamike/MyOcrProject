#!/usr/bin/env python
# -*- coding:utf8 -*-
import configparser
import datetime

import os


class LogUtils(object):
    def __init__(self):
        conf = configparser.ConfigParser()
        file = os.getcwd() + "/Config.conf";
        conf.read(file)
        self.fileDir = conf.get("path", "log_dir")
        self.file = open(self.fileDir, 'a+', encoding='utf-8')

    def printLog(self, logMsg):
        print(logMsg)
        self.file.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + logMsg + "\n")

log=LogUtils()
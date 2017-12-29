#!/usr/bin/env python
# -*- coding:utf8 -*-
import configparser

from utils.LogUtils import log
from MultThreadBaiduImgs import *


class OcrMain(object):
    def __init__(self):
        print("init")


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    file = os.getcwd() + "/Config.conf"
    conf.read(file)
    search_word_dir = conf.get('path', 'search_word')
    log.printLog("关键词路径：" + str(search_word_dir))

    with open(search_word_dir, 'rb') as file:
        for line in file.readlines():
            startLoadImgs(line, conf.get('path', 'down_dir'))

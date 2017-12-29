#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import configparser

from aip import AipOcr
import json
from utils.LogUtils import log


# conf = configparser.ConfigParser()
# file=os.getcwd()+"/Config.conf";
#
# conf.read(file)
# session=conf.sections()
# print("section",session)
# print(conf.get("baidu","a"))

class BaiduORC(object):
    def __init__(self):
        # self.imgUrl = "http://pursuege.oss-cn-shenzhen.aliyuncs.com/img/timg.jpg";
        conf = configparser.ConfigParser()
        file = os.getcwd() + "/Config.conf"
        conf.read(file)
        keyFile = conf.get('path', 'key_path')
        self.keyArray = [['10506105', 'l6xFr9MFZrj1I6XkObWf7jqN', '3iDMlsadAXqy5CIOGIjW2pnr4KrHEey3']]
        with open(keyFile, 'rb') as file:
            for line in file.readlines():
                if line.split():
                    # 最后的可以列表
                    self.keyArray.append(line.split())

        self.keyIndex = 0
        self.client = AipOcr(self.keyArray[self.keyIndex][0], self.keyArray[self.keyIndex][1],
                             self.keyArray[self.keyIndex][2])
        # 定义参数变量
        self.options = {
            'detect_direction': 'true',
            'language_type': 'CHN_ENG',
        }

    def decodeImgUrl(self, imgUrl):
        jsonStr = self.client.basicGeneral(imgUrl, self.options)

        # jsonStr="{'log_id': 1902239055352749612, 'direction': 0, 'words_result_num': 2, 'words_result': [{'words': '再不走'}, {'words': '就打死你'}]}"
        jsonStr = str(jsonStr)
        print(jsonStr)
        jsonStr = jsonStr.replace("'", "\"")

        resoult = json.loads(jsonStr)
        return resoult

    def setNextKeySecret(self):
        self.keyIndex += 1
        if self.keyIndex >= len(self.keyArray):
            self.keyIndex = 0
        log.printLog("重置账号：" + str(self.keyIndex))
        self.client = AipOcr(self.keyArray[self.keyIndex][0], self.keyArray[self.keyIndex][1],
                             self.keyArray[self.keyIndex][2])


baidu_ocr = BaiduORC()

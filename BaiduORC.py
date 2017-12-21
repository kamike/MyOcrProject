#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import configparser

from aip import AipOcr
import json


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
        self.client = AipOcr("10506105", "l6xFr9MFZrj1I6XkObWf7jqN", "3iDMlsadAXqy5CIOGIjW2pnr4KrHEey3 ")
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

baidu_ocr=BaiduORC()
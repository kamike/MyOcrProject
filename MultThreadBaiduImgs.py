#!/usr/bin/env python
# -*- coding:utf8 -*-
import hashlib
import itertools
import urllib
import requests
import os
import re
import sys
from PIL import Image

from sql.FileBean import FileBean
from sql.OcrBean import OcrBean
from sql.SQLUtils import SQLUtils
from utils.LogUtils import log
from BaiduORC import baidu_ocr

import uuid

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

search_url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
utils = SQLUtils()

# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}


# 解码图片URL
def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)


# 生成网址列表
def buildUrls(word):
    word = urllib.parse.quote(word)
    # url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (search_url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls


# 解析JSON获取图片URL
re_url = re.compile(r'"objURL":"(.*?)"')


def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls


def downImg(imgUrl, dirpath, name):
    filename = os.path.join(dirpath, name)
    # sq操作


    try:
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == "4":
            log.printLog("状态码不正确：" + str(res.status_code), ":", imgUrl)
            return -1
    except Exception as e:
        log.printLog("抛出异常：" + imgUrl + "," + e.__str__())
        return -1
    with open(filename, "wb") as f:
        f.write(res.content)
        f.close()

    file = open(filename, "rb")
    # 添加一条数据积累
    fileBean = FileBean(imgUrl, name, dirpath, str(file.__sizeof__()),
                        hashlib.md5(file.read()).hexdigest(),
                        '0', '0', getFileNameEnd(imgUrl))
    return utils.addTableFile(fileBean)


def mkDir(dirName):
    dirpath = os.path.join(sys.path[0], dirName)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath


def getFileNameEnd(url):
    return url[url.rindex('.'):len(url)]


def startLoadImgs(word, imgDirpath):
    urls = buildUrls(word)
    index = 0
    for url in urls:
        print("正在请求：", url)

        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:  # 没有图片则结束
            break
        for url in imgUrls:
            print(url)
            fileName = str(index) + "__" + str(uuid.uuid1()) + getFileNameEnd(url)
            index = downImg(url, imgDirpath, fileName)
            if index >= 0:
                log.printLog("已下载 %s 张" % index)
                try:
                    content = baidu_ocr.decodeImgUrl(url)
                    utils.addTableOcr(
                        OcrBean(content['words_result'], index, word, 'baidu', search_url))
                except Exception as e:
                    # 解析失败了
                    utils.deleteFile(index)
                    os.remove(fileName)
                    log.printLog("解析失败了" + imgUrls)

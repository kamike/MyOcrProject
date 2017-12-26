#!/usr/bin/env python
# -*- coding:utf8 -*-
import pymysql


class SQLUtils(object):
    def __init__(self):
        print("init=====sql=")
        self.dataBases = pymysql.connect("39.108.177.124", "wangtao", "PPYY0264", "ocr_data", charset='utf8')
        self.cursor = self.dataBases.cursor()
        self.tbl_file = "tbl_file"
        self.tbl_ocr = "tbl_ocr"

    def exeSelect(self, tbl, where):
        sql = "select * from " + tbl + " where " + where
        self.cursor.execute(where)

    def addTableFile(self, fileBean):
        sql = "insert into " + self.tbl_file + "(" + fileBean.__getParaStr__() + ") values(" + fileBean.__str__() + ")";
        print(sql)
        try:
            self.cursor.execute(sql)
            self.dataBases.commit()
            return int(self.cursor.lastrowid)
        except:
            self.dataBases.rollback()
            print("exception====")
            return -1

    def addTableOcr(self, OcrBean):
        sql = "insert into " + self.tbl_ocr + "(" + OcrBean.__getParaStr__() + ") values(%s,%s,%s,%s,%s,%s)"
        print(sql)
        try:
            self.cursor.execute(sql, (OcrBean.content, OcrBean.file_id, OcrBean.key_word, OcrBean.type,
                                      OcrBean.search_url, OcrBean.create_date))
            self.dataBases.commit()
            return int(self.cursor.lastrowid)
        except Exception as e:
            self.dataBases.rollback()
            print("exception====")
            return -1

    def closedAll(self):
        print("close-====")
        self.cursor.close()

    def deleteFile(self, index):
        sql = "DELETE FROM tbl_file WHERE _id=" + index
        try:
            self.cursor.execute(sql)
            self.dataBases.commit()
        except:
            self.dataBases.rollback()
            print("exception====")

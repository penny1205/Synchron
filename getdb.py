#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'penny'

import configparser,pymysql
import sys

class GetDB:
    '''配置数据库IP，端口等信息，获取数据库连接'''
    def __init__(self, ini_file, db):
        config = configparser.ConfigParser()

        # 从配置文件中读取数据库服务器IP、域名，端口
        config.read(ini_file,encoding='utf-8')
        self.host = config[db]['host']
        self.port = config[db]['port']
        self.user = config[db]['user']
        self.passwd = config[db]['passwd']
        self.db = config[db]['db']
        # self.charset = config[db]['charset']

    def get_conn(self):
        try:
            conn = pymysql.Connect(host=self.host, port=int(self.port), user=self.user, password=self.passwd)
            return conn
        except Exception as e:
            print('%s', e)
            sys.exit()
            
    def dbinfo(self):
        return self.host,self.port,self.user,self.passwd

if __name__ == '__main__':
    db = GetDB('./config.ini','DATABASE1')
    db.get_conn()
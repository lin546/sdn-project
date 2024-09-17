"""
 @file     sqlhelper.py                                                       
 @brief    本文件用提供对数据库初始化的函数                                                  
 Details.                                                                  
"""
import pymysql


class sqlInit(object):

    @staticmethod
    def open():
        host = app.config.get("HOST")
        uname = app.config.get("USER")
        pwd = app.config.get("PWD")
        database = app.config.get("DB")
        conn = pymysql.connect(host, uname, pwd, database)
        cursor = conn.cursor()
        return conn,cursor
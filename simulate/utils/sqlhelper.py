"""
 @file     sqlhelper.py                                                       
 @brief    本文件用提供对数据库操作的函数                                                  
 Details.                                                                  
"""
import pymysql
from flask import current_app

class sqlHelper(object):

    @staticmethod
    def open():
        host = current_app.config['HOST']
        uname = current_app.config['USER']
        pwd = current_app.config['PWD']
        database = current_app.config['DB']
        conn = pymysql.connect(host, uname, pwd, database)
        cursor = conn.cursor()
        return conn,cursor
        
    @staticmethod
    def add(sql,args):
        conn,cursor = sqlHelper.open()
        rowcount = cursor.execute(sql,args)
        sqlHelper.close(conn,cursor)
        return rowcount  

    @staticmethod
    def close(conn,cursor):
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def fetch_one(sql,args):
        conn,cursor = sqlHelper.open()
        cursor.execute(sql,args)
        obj =  cursor.fetchone()
        sqlHelper.close(conn,cursor)
        return obj
    
    @staticmethod
    def fetch_all(sql,args):
        conn,cursor = sqlHelper.open()
        cursor.execute(sql,args)
        obj =  cursor.fetchall()
        sqlHelper.close(conn,cursor)

        return obj

    @staticmethod
    def update(sql,args):
        from sqlinit import db
        conn,cursor = sqlHelper.open()
        rowcount = cursor.execute(sql,args)
        sqlHelper.close(conn,cursor)
        return rowcount  
    
    @staticmethod
    def delete(sql,args):
        from sqlinit import db
        conn,cursor = sqlHelper.open()
        rowcount = cursor.execute(sql,args)
        sqlHelper.close(conn,cursor)
        return rowcount  
    
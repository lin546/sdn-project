"""
 @file     sqlhelper.py                                                       
 @brief    本文件用提供对数据库操作的函数                                                  
 Details.                                                                  
"""
import pymysql


class sqlHelper(object):

    @staticmethod
    def open():
        from simulate import app
        host = app.config.get("HOST")
        uname = app.config.get("USER")
        pwd = app.config.get("PWD")
        database = app.config.get("DB")
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
    
# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.07.15

import pymysql

"""
MySQL数据库基础操作类
"""
class MysqlHelper(object):
    conn = None
    _instance = None

    def __init__(self, host, port, db, user, password, charset='utf8'):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.charset = charset

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)

        return cls._instance

    """
    数据库连接
    """
    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=int(self.port), user=self.user, password=self.password,
                    db=self.db, charset=self.charset)
        self.cursor = self.conn.cursor(cursor = pymysql.cursors.DictCursor)

    """
    数据库关闭连接资源
    """
    def close(self):
        self.cursor.close()
    
    """
    获取单条数据
    """
    def fetchOne(self, sql, params=()):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e)
        return result
    
    """
    获取多条数据
    """
    def fetchAll(self, sql, params=()):
        result = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e)
        return result

    """
    插入数据
    """
    def insert(self, sql, params=()):
        return self.__edit(sql, params)

    """
    更新数据
    """
    def update(self, sql, params=()):
        return self.__edit(sql, params)

    """
    删除数据
    """
    def delete(self, sql, params=()):
        return self.__edit(sql, params)
    
    """
    Execute操作
    """
    def __edit(self, sql, params):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e)
        return count

if __name__ == '__main__':
    pass
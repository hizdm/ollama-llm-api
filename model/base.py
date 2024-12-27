# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.07.15

from library.util import util
from library.mysql import mysqlhelper

"""
@brief Base Model
@param conf_file string 自定义配置文件
@param node_name string 节点名称
"""
class BaseModel():
    def __init__(self, conf_file='global.ini', node_name='mysql_r'):
        self.host = util.fetch_conf(conf_file, node_name, 'host')
        self.port = util.fetch_conf(conf_file, node_name, 'port')
        self.db = util.fetch_conf(conf_file, node_name, 'db')
        self.user = util.fetch_conf(conf_file, node_name, 'user')
        self.password = util.fetch_conf(conf_file, node_name, 'password')
        self.charset = util.fetch_conf(conf_file, node_name, 'charset')

        self.objMysql = mysqlhelper.MysqlHelper(self.host, self.port, self.db, self.user, self.password, self.charset)

    """
    @brief Fetch One
    """
    def fetchOne(self, sql, params):
        result = self.objMysql.fetchOne(sql, params)

        return result
    
    """
    @brief Fetch All
    """
    def fetchAll(self, sql, params):
        result = self.objMysql.fetchAll(sql, params)

        return result

    """
    @brief Insert
    """
    def insert(self, sql, params):
        result = self.objMysql.insert(sql, params)

        return result

    """
    @brief Update
    """
    def update(self, sql, params):
        result = self.objMysql.update(sql, params)

        return result

    """
    @brief Delete
    """
    def delete(self, sql, params):
        result = self.objMysql.delete(sql, params)

        return result


if __name__ == '__main__':
    pass
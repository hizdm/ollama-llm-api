# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.07.15

import os
import configparser

"""
@brief 获取文件配置信息
@param file_name 配置文件名称
@param section 节点名称
@param option Item
"""
def fetch_conf(file_name = '', section = '', option = ''):
    file = os.path.abspath(os.path.join(os.getcwd(), 'conf', file_name))

    config = configparser.ConfigParser()
    config.read(file, encoding='utf-8')
    result = config.get(section, option)

    return result

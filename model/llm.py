# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.07.15

from model.base import BaseModel

"""
@brief LLM Model
"""
class LlmModel(BaseModel):
    def __init__(self, conf_file='global.ini', node_name='mysql_r'):
        # 调用父类的初始化方法并传递参数
        super().__init__(conf_file, node_name)


if __name__ == '__main__':
    pass

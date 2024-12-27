# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.07.15
import os
import tornado.log
from tornado.options import options

# 格式化日志输出格式
# 默认是这种的：[I 160807 09:27:17 web:1971] 200 GET / (::1) 7.00ms
# 格式化成这种的：[2016-08-07 09:38:01 执行文件名:执行函数名:执行行数 日志等级] 内容消息
class LogFormatter(tornado.log.LogFormatter):
	def __init__(self):
		super(LogFormatter, self).__init__(
			fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
			datefmt='%Y-%m-%d %H:%M:%S'
        )

# options.log_file_prefix = os.path.join(os.path.dirname(__file__), 'log.txt')
# options.log_rotate_mode = 'time' # 切割方式：按时间
# options.log_rotate_when = 'D' # 切割单位：天
# options.log_rotate_interval = 1 # 间隔值：1天

# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.07.15

from __future__ import absolute_import
import os
import tornado.ioloop
import tornado.web
from tornado.options import options, define
import tornado.autoreload
import logging
import router.urls as urls
from library.util import util
from library.log import loghelper

define('port', default=int(util.fetch_conf('global.ini', 'app', 'port')), help='监听端口')   # APP端口
define('debug', default=util.fetch_conf('global.ini', 'app', 'debug'), help='是否开启调试')  # APP模式 True:调试, False:关闭调试
options.log_file_prefix = os.path.join(os.path.dirname(__file__), 'log/log.txt')    # 日志路径
options.log_rotate_mode = util.fetch_conf('global.ini', 'log', 'mode')              # 日志切割方式：time:按时间
options.log_rotate_when = util.fetch_conf('global.ini', 'log', 'when')              # 日志切割单位：D:天
options.log_rotate_interval = int(util.fetch_conf('global.ini', 'log', 'interval')) # 日志间隔值：1天

"""
@brief 404
"""
class My404Handler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_status(404)
        self.render('404.html')

"""
@brief Main
"""
def main():
    options.parse_command_line()
    app = tornado.web.Application(
        urls.urls, # 路由分发
        template_path=os.path.join(os.path.dirname(__file__), "template"), # 模板存放位置
        static_path=os.path.join(os.path.dirname(__file__), "static"), # 静态文件存放位置
        debug=options.debug, # 热加载调试（True:开启; False:关闭）
        default_handler_class=My404Handler) # 默认404

    [i.setFormatter(loghelper.LogFormatter()) for i in logging.getLogger().handlers] # 日志
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()

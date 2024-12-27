# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.07.15

import tornado.web
from library.jwt import jwt as myjwt
import jwt

class BaseHandler(tornado.web.RequestHandler):
	# 配置请求头，允许跨域，否则在浏览器调用的时候报错误，同时还得加上允许Authorization字段过来
	def setHeaders(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
		self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")

	# 这个函数是必要的，有些浏览器或者测试工具在访问之前都会预先访问，你不写的话会导致出错的
	# 例如vue一般需要访问options方法
	def options(self):
		self.finish()

	"""
    通过分析请求头部的Authorization中的数据 判断是否过期 
    并解析出用户的相关信息
	"""
	def getHeaders(self):
		try:
			auth_token = self.request.headers.get("Authorization")
			if not auth_token:
				self.set_status(401)
				# self.write({"code": 401, "message": "未授权", "data": []})
				return
			# 传过来的是字符串 我们需要转换成字节，才能解密
			auth_token = bytes(auth_token, encoding="utf8")
			auth_token = myjwt.decode_token(auth_token)
		except jwt.exceptions.ExpiredSignatureError as e:
			self.set_status(403)
			# self.write({"code": 403, "message": "拒绝访问", "data": []})
			return

		return auth_token




	

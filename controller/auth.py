# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.11.11

import sys
import json
from library.jwt import jwt as myjwt
from controller.base import BaseHandler
from model.llm import LlmModel


"""
JWT Auth
"""
class AuthHandler(BaseHandler):
	"""
	@brief 认证
	"""
	def post(self):
		try:
			data   = json.loads(self.request.body)
			uid    = data.get('uid', None)
			secret = data.get('secret', None)
		except json.JSONDecodeError:
			self.set_status(400)
			self.write({"code":400102, "message":"invalid JSON", "data":{}})
			return

		if uid is None:
			self.write({"code":400103, "message":"illegal request", "data":{}})
			return
		if secret is None:
			self.write({"code":400104, "message":"illegal request", "data":{}})
			return

		objInstance = LlmModel("global.ini", "mysql_r")
		userInfo = objInstance.fetchOne("select * from t_consumer where consumer_no = %s", [uid])
		if userInfo is None:
			self.write({"code":400105, "message":"illegal request", "data":{}})
			return
		else:
			if userInfo.get("password") != secret.strip():
				self.write({"code":400106, "message":"illegal request", "data":{}})
				return
			else:
				auth_token = myjwt.encode_token(uid)

		self.write({"code":0, "message":"success", "data":auth_token})
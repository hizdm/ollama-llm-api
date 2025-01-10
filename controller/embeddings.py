# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.11.19

import sys
import json
from ollama import Client
from library.util import util
from controller.base import BaseHandler

"""
LLM Embeddings
"""
class EmbeddingsHandler(BaseHandler):
	def post(self):
		try:
			data    = json.loads(self.request.body)  # 请求数据
			model   = data.get('model', 'nomic-embed-text:latest') # 模型名称
			role    = data.get('role', 'user')       # 角色名称
			content = data.get('content', 'Hello')   # 编码内容
		except json.JSONDecodeError:
			self.set_status(400)
			self.write({'code':400201, 'message':'invalid json', 'data':[]})
			return
		
		output = {
			"code": 0,
			"message": "success",
			"data": {}
		}

		# Params
		if model is None:
			output = {'code':400203, 'message':'model is null', 'data':[]}
			self.write(json.dumps(output))
			return

		# # Auth
		# authToken = self.getHeaders()
		# if not authToken:
		# 	self.write({'code':400201, 'message':'signature error', 'data':[]})
		# 	return
		# else:
		# 	payload = authToken.get('payload')
		# 	if not payload:
		# 		self.write({'code':400204, 'message':'signature error', 'data':[]})
		# 		return
		# 	else:
		# 		uid = payload.get('uid')

		# Strategy
		# todo

		# Embeddings
		try:
			client = Client(host=util.fetch_conf('global.ini', 'llm', 'host'))
			response = client.embeddings(model=model, prompt=content)
			output["data"] = response
		except Exception as e:
			output = {
				"code": 400444,
				"message": e,
				"data": {}
			}

		self.write(json.dumps(output))
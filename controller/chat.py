# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.11.11

import sys
import json
from ollama import Client
from library.util import util
from controller.base import BaseHandler
from controller.prompt import PromptHandler

"""
Ollama Chat
"""
class ChatHandler(BaseHandler):
	def post(self):
		try:
			data    = json.loads(self.request.body)  # 请求数据
			model   = data.get('model', None)        # 模型名称
			role    = data.get('role', 'user')       # 角色名称
			message = data.get('message', 'Hello')   # 对话内容[输入内容(默认Hello)->提示工程处理]
			pid     = data.get('pid', None)          # 项目标识
			prompt  = data.get('prompt', None)       # 提示工程标识
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
		if pid is None:
			output = {'code':400202, 'message':'pid is null', 'data':[]}
			self.write(json.dumps(output))
			return
		if model is None:
			output = {'code':400203, 'message':'model is null', 'data':[]}
			self.write(json.dumps(output))
			return

		# Auth
		authToken = self.getHeaders()
		if not authToken:
			self.write({'code':400601, 'message':'signature error', 'data':[]})
			return
		else:
			payload = authToken.get('payload')
			if not payload:
				self.write({'code':400602, 'message':'signature error', 'data':[]})
				return
			else:
				uid = payload.get('uid')

		# Strategy
		# todo

		# Prompt
		if prompt is not None:
			promptInstance = PromptHandler()
			promptInfo = promptInstance.getPromptInfo({"prompt_key": prompt})
			if promptInfo is not None:
				promptTemplate = promptInfo.get("prompt_data", None)
				if promptTemplate is not None:
					message = promptTemplate.replace("{%S%}", message)

		# Chat
		try:
			client = Client(host=util.fetch_conf('global.ini', 'llm', 'host'))
			response = client.chat(model=model, 
				messages=[{
					"role": role,
					"content": message
				}],
				options={"temperature": 0})
			output["data"] = response
		except Exception as e:
			output = {
				"code": 400444,
				"message": "system error",
				"data": {}
			}

		self.write(json.dumps(output))
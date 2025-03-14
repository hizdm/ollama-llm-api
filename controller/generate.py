# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.11.11

import sys
import json
from ollama import Client
from library.util import util
from controller.base import BaseHandler
from controller.prompt import PromptHandler
from controller.strategy import StrategyHandler

"""
Ollama Generate
"""
class GenerateHandler(BaseHandler):
	def post(self):
		try:
			data    = json.loads(self.request.body)  # 请求数据
			model   = data.get('model', None)        # 模型名称
			role    = data.get('role', 'user')       # 角色名称
			content = data.get('content', 'Hello')   # 对话内容[输入内容(默认Hello)->提示工程处理]
			prompt  = data.get('prompt', None)       # 提示工程标识
			is_stream   = data.get('is_stream', 0)   # 是否流式输出
			temperature = data.get('temperature', float(util.fetch_conf('global.ini', 'generate', 'temperature')))   # 温度
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
		objStrategy = StrategyHandler(uid)
		s1 = objStrategy.sInterval({})
		if s1['code'] != 0:
			self.write(json.dumps(s1))
			return
		s2 = objStrategy.sTimetotal({})
		if s2['code'] != 0:
			self.write(json.dumps(s2))
			return

		# Prompt
		if prompt is not None:
			promptInstance = PromptHandler()
			promptInfo = promptInstance.getPromptInfo({"prompt_key": prompt})
			if promptInfo is not None:
				promptTemplate = promptInfo.get("prompt_data", None)
				if promptTemplate is not None:
					content = promptTemplate.replace("{%S%}", content)

		# Generate
		try:
			client = Client(host=util.fetch_conf('global.ini', 'llm', 'host'))
			#response = client.generate(model=model, prompt=content)
			#output["data"] = response['response']
			response = client.generate(model=model, 
				prompt=content,
				stream=False,
				options={
				    "temperature": temperature, 
					"num_keep": int(util.fetch_conf('global.ini', 'generate', 'num_keep')),
					"num_ctx": int(util.fetch_conf('global.ini', 'generate', 'num_ctx')),
				})
			#output["data"] = response['response']
			if is_stream == 1:
				for chunk in response:
					self.write(chunk['response'])
					self.flush()
			else:
				output["data"] = response['response']
				self.write(json.dumps(output, ensure_ascii=False))

		except Exception as e:
			output = {
				"code": 400444,
				"message": "system error",
				"data": {}
			}

			self.write(json.dumps(output, ensure_ascii=False))

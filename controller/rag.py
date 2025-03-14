# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.11.19

import sys
import json
import chromadb
from ollama import Client
from library.util import util
from library.chromadb import chromahelper
from controller.base import BaseHandler
from controller.strategy import StrategyHandler

"""
LLM RAG
"""
class RagHandler(BaseHandler):
	def post(self):
		try:
			data           = json.loads(self.request.body)                           # 请求数据
			role           = data.get('role', 'user')                                # 角色名称
			number         = data.get('number', 1)                                   # 查询数量
			content        = data.get('content', 'hello')                            # 输入内容
			generateModel  = data.get('generate_model', None)                        # 生成模型
			embeddingModel = data.get('embedding_model', 'nomic-embed-text:latest')  # 编码模型
			collectionName = data.get('collection', None)                            # 集合名称
			is_stream      = data.get('is_stream', 0)                                # 是否流式输出
			temperature    = data.get('temperature', float(util.fetch_conf('global.ini', 'generate', 'temperature')))   # 温度
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
		if generateModel is None:
			output = {'code':400203, 'message':'generate model is null', 'data':[]}
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
	
		# Generate
		try:
			objChroma = chromahelper.ChromaHelper()
			ollama = Client(host=util.fetch_conf('global.ini', 'llm', 'host'))
			queryEmbedding = ollama.embeddings(model=embeddingModel, prompt=content)
			queryResult = objChroma.queryDocuments(collectionName, queryEmbedding['embedding'], number)
			print(queryResult)

			if len(queryResult['documents'][0]) > 0:
				queryContent = ""
				queryContent = ', '.join(queryResult['documents'][0])
				content=f"基于这些内容:{queryContent}. 回答这个问题:{content}"
			response = ollama.generate(model=generateModel, 
				prompt=content,
				stream = True if is_stream == 1 else False,
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
				output["data"] = response.message.content
				self.write(json.dumps(output, ensure_ascii=False))

		except Exception as e:
			output = {
				"code": 400444,
				"message": e,
				"data": {}
			}
			self.write(json.dumps(output, ensure_ascii=False))

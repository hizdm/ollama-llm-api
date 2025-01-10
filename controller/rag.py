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

		# # Auth
		# authToken = self.getHeaders()
		# if not authToken:
		# 	self.write({'code':400601, 'message':'signature error', 'data':[]})
		# 	return
		# else:
		# 	payload = authToken.get('payload')
		# 	if not payload:
		# 		self.write({'code':400602, 'message':'signature error', 'data':[]})
		# 		return
		# 	else:
		# 		uid = payload.get('uid')

		# Strategy
		# todo

		# Generate
		try:
			objChroma = chromahelper.ChromaHelper()
			ollama = Client(host=util.fetch_conf('global.ini', 'llm', 'host'))
			queryEmbedding = ollama.embeddings(model=embeddingModel, prompt=content)
			queryResult = objChroma.queryDocuments(collectionName, queryEmbedding['embedding'], number)

			if len(queryResult['documents'][0]) > 0:
				queryContent = ""
				queryContent = ', '.join(queryResult['documents'][0])
				content=f"基于这些内容:{queryContent}. 回答这个问题:{content}"
			response = ollama.generate(model=generateModel, prompt=content)
			output["data"] = response['response']
		except Exception as e:
			output = {
				"code": 400444,
				"message": e,
				"data": {}
			}

		self.write(json.dumps(output))
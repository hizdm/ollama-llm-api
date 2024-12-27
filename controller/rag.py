# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.11.19

import sys
import json
import chromadb
from ollama import Client
from library.util import util
from controller.base import BaseHandler

"""
LLM RAG
"""
class RagHandler(BaseHandler):
	def post(self):
		try:
			data    = json.loads(self.request.body)  # 请求数据
			model   = data.get('model', None)        # 模型名称
			role    = data.get('role', 'user')       # 角色名称
			content = data.get('content', 'Hello')   # 对话内容
			pid     = data.get('pid', None)          # 项目标识
			collectionName = data.get('collection', 'test_collection')  # 集合名称
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
		embeddingModel = 'nomic-embed-text:latest'
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

		# Generate
		try:
			ollamaClient = Client(host=util.fetch_conf('global.ini', 'llm', 'host'))
			queryResponse = ollamaClient.embeddings(model=embeddingModel, prompt=content)

			chromaClient = chromadb.Client()
			collection = chromaClient.get_or_create_collection(collectionName)
			queryResult = collection.query(
				query_embeddings=[queryResponse['embedding']],
				n_results=1
			)
			if len(queryResult['documents'][0]) > 0:
				query = queryResult['documents'][0][0]
				content=f"基于这些内容:{query}. 回答这个问题:{content}"

			response = ollamaClient.generate(model=model, prompt=content)
			output["data"] = response
		except Exception as e:
			output = {
				"code": 400444,
				"message": e,
				"data": {}
			}

		self.write(json.dumps(output))
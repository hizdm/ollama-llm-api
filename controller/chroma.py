# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2025.01.09

import sys
import json
import chromadb
from ollama import Client
from library.chromadb import chromahelper
from library.util import util
from controller.base import BaseHandler


"""
Create Collection
Example：
{
  "collection": "test-005"
}
"""
class CreateCollectionHandler(BaseHandler):
	def post(self):
		try:
			data       = json.loads(self.request.body)  # 请求数据
			collection = data.get('collection', None)   # 集合名称
		except json.JSONDecodeError:
			self.set_status(400)
			self.write({'code':400201, 'message':'invalid json', 'data':[]})
			return
		
		objChroma = chromahelper.ChromaHelper()
		if not collection:
			output = {"code":400802, "message":"collection cannot be empty.", "data":[]}
			self.write(json.dumps(output))
			return
		else:
			if objChroma.createCollection(collection) == False:
				output = {"code":400803, "message":f"Collection '{collection}' already exists.", "data":[]}
				self.write(json.dumps(output))
				return
			else:
				output = {"code":0, "message":f"Collection '{collection}' create success.", "data":[]}
				self.write(json.dumps(output))
				return

"""
AddDocument
Example：
{
  "collection": "test-005",
  "ids": ["001", "002", "003"],
  "documents": ["xiaoming documents", "xiaohong documents", "xiaoqiang documents"],
  "metadatas": [{"source": "001.txt"}, {"source": "002.txt"}, {"source": "003.txt"}]
}
"""
class AddDocumentHandler(BaseHandler):
	def post(self):
		try:
			data       = json.loads(self.request.body)                 # 请求数据
			ids        = data.get('ids', None)                         # 文档id
			documents  = data.get('documents', None)                   # 文档数据
			metadatas  = data.get('metadatas', None)                   # 文档元数据
			collection = data.get('collection', None)                  # 集合名称
			model      = data.get('model', 'nomic-embed-text:latest')  # 模型名称(默认nomic-embed-text:latest)
		except json.JSONDecodeError:
			self.set_status(400)
			self.write({'code':400201, 'message':'invalid json', 'data':[]})
			return
		
		output = {
			"code": 0,
			"message": "success",
			"data": []
		}

		if not ids or not documents or len(ids) != len(documents):
			output = {"code":400801, "message":"'ids' and 'documents' must have the same length and cannot be empty.", "data":[]}
			self.write(json.dumps(output))
			return

		objChroma = chromahelper.ChromaHelper()
		if not collection:
			output = {"code":400802, "message":"collection cannot be empty.", "data":[]}
			self.write(json.dumps(output))
			return
		else:
			if objChroma.getCollection(collection) == False:
				output = {"code":400804, "message":"collection does not exist.", "data":[]}
				self.write(json.dumps(output))
				return



		ollama = Client(host=util.fetch_conf('global.ini', 'llm', 'host'))
		embeddings = []
		for i in documents:
			iembedding = ollama.embeddings(model=model, prompt=i)
			embeddings.append(iembedding['embedding'])

		
		objChroma.addDocuments(collection, ids, documents, metadatas, embeddings)
		output = {"code":0, "message":f"Added {len(documents)} documents to '{collection}'.", "data":[len(documents)]}
		self.write(json.dumps(output))

"""
QueryDocument
Example：
{
  "collection": "test-005",
  "number": 3,
  "query": "hong"
}
"""
class QueryDocumentHandler(BaseHandler):
	def post(self):
		try:
			data       = json.loads(self.request.body)                 # 请求数据
			query      = data.get('query', None)                       # 查询内容
			number     = data.get('number', 5)                         # 查询数量
			collection = data.get('collection', None)                  # 集合名称
			model      = data.get('model', 'nomic-embed-text:latest')  # 模型名称(默认nomic-embed-text:latest)
		except json.JSONDecodeError:
			self.set_status(400)
			self.write({'code':400201, 'message':'invalid json', 'data':[]})
			return

		objChroma = chromahelper.ChromaHelper()
		if not collection:
			output = {"code":400802, "message":"collection cannot be empty.", "data":[]}
			self.write(json.dumps(output))
			return
		else:
			if objChroma.getCollection(collection) == False:
				output = {"code":400804, "message":"collection does not exist.", "data":[]}
				self.write(json.dumps(output))
				return

		if not query:
			output = {"code":400805, "message":"query cannot be empty.", "data":[]}
			self.write(json.dumps(output))
			return

		ollama = Client(host=util.fetch_conf('global.ini', 'llm', 'host'))
		queryEmbedding = ollama.embeddings(model=model, prompt=query)
		queryResult = objChroma.queryDocuments(collection, queryEmbedding['embedding'], number)
		output = {"code":0, "message":f"success", "data":queryResult}
		self.write(json.dumps(output))

"""
Delete Collection
Example：
{
  "collection": "test-005"
}
"""
class DeleteCollectionHandler(BaseHandler):
	def post(self):
		try:
			data       = json.loads(self.request.body)  # 请求数据
			collection = data.get('collection', None)   # 集合名称
		except json.JSONDecodeError:
			self.set_status(400)
			self.write({'code':400201, 'message':'invalid json', 'data':[]})
			return
		
		objChroma = chromahelper.ChromaHelper()
		if not collection:
			output = {"code":400802, "message":"collection cannot be empty.", "data":[]}
			self.write(json.dumps(output))
			return
		else:
			if objChroma.getCollection(collection) == False:
				output = {"code":400804, "message":"collection does not exist.", "data":[]}
				self.write(json.dumps(output))
				return
			if objChroma.deleteCollection(collection) == False:
				output = {"code":400806, "message":f"Collection '{collection}' delete error.", "data":[]}
				self.write(json.dumps(output))
				return
			else:
				output = {"code":0, "message":f"Collection '{collection}' delete success.", "data":[]}
				self.write(json.dumps(output))
				return
# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.11.11

from controller.base import BaseHandler
from model.llm import LlmModel

"""
Prompt Project
"""
class PromptHandler(BaseHandler):
	def __init__(self, strConf = 'global.ini', strDataBase = 'mysql_r'):
		self.objMysql = LlmModel(strConf, strDataBase)


	"""
	@brief 获取提示工程模板信息
	"""
	def getPromptInfo(self, params):
		promptInfo = self.objMysql.fetchOne('select * from t_prompt where prompt_key = %s and status = 1', [params.get('prompt_key', '')])

		return promptInfo
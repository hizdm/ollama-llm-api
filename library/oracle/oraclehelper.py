# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.11.13

import cx_Oracle
import threading

"""
Oracle数据库基础操作类
"""
class OracleDB:
	# 单例实例
	_instance = None
	_lock = threading.Lock()  # 用于线程安全的单例

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			with cls._lock:
				if not cls._instance:
					cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self, user, password, dsn, encoding="UTF-8"):
		if not hasattr(self, "_is_initialized"):  # 确保__init__只执行一次
			self._is_initialized = True
			self.user = user
			self.password = password
			self.dsn = dsn
			self.encoding = encoding
			self.connection = None
			self.cursor = None

	def connect(self):
		"""建立数据库连接"""
		try:
			self.connection = cx_Oracle.connect(
				self.user,
				self.password,
				self.dsn,
				encoding=self.encoding
			)
			self.cursor = self.connection.cursor()
			print("数据库连接成功")
		except cx_Oracle.DatabaseError as e:
			print("数据库连接失败:", e)
			raise

	def disconnect(self):
		"""关闭数据库连接"""
		if self.cursor:
			self.cursor.close()
		if self.connection:
			self.connection.close()
			print("数据库连接已关闭")

	def execute_query(self, query, params=None):
		"""执行查询语句并返回结果"""
		try:
			self.cursor.execute(query, params or {})
			result = self.cursor.fetchall()
			return result
		except cx_Oracle.DatabaseError as e:
			print("查询执行失败:", e)
			raise

	def execute_non_query(self, query, params=None):
		"""执行非查询语句（插入、更新、删除）"""
		try:
			self.cursor.execute(query, params or {})
			self.connection.commit()
			print("非查询操作成功执行")
		except cx_Oracle.DatabaseError as e:
			print("非查询操作失败:", e)
			self.connection.rollback()
			raise

	def execute_many(self, query, params_list):
		"""批量执行语句"""
		try:
			self.cursor.executemany(query, params_list)
			self.connection.commit()
			print("批量操作成功执行")
		except cx_Oracle.DatabaseError as e:
			print("批量操作失败:", e)
			self.connection.rollback()
			raise

	def call_procedure(self, proc_name, params):
		"""调用存储过程"""
		try:
			self.cursor.callproc(proc_name, params)
			self.connection.commit()
			print("存储过程调用成功")
		except cx_Oracle.DatabaseError as e:
			print("存储过程调用失败:", e)
			raise

	def call_function(self, func_name, return_type, params):
		"""调用存储函数"""
		try:
			result = self.cursor.callfunc(func_name, return_type, params)
			return result
		except cx_Oracle.DatabaseError as e:
			print("存储函数调用失败:", e)
			raise

	def fetch_one(self, query, params=None):
		"""获取单条记录"""
		try:
			self.cursor.execute(query, params or {})
			result = self.cursor.fetchone()
			return result
		except cx_Oracle.DatabaseError as e:
			print("获取单条记录失败:", e)
			raise

	def fetch_many(self, query, size, params=None):
		"""获取指定数量的记录"""
		try:
			self.cursor.execute(query, params or {})
			result = self.cursor.fetchmany(size)
			return result
		except cx_Oracle.DatabaseError as e:
			print("获取多条记录失败:", e)
			raise

# 使用示例
if __name__ == "__main__":
	# 请将以下信息替换为你的实际数据库连接信息
	db = OracleDB(user="your_user", password="your_password", dsn="your_dsn")
	
	db.connect()
	try:
		# 执行查询
		result = db.execute_query("SELECT * FROM your_table WHERE id = :id", {"id": 1})
		print(result)
		
		# 执行非查询
		db.execute_non_query("UPDATE your_table SET name = :name WHERE id = :id", {"name": "New Name", "id": 1})
	finally:
		db.disconnect()

# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.07.15

import redis

"""
Redis基础操作类
"""
class RedisHelper():
	redis_conn = None
	"""
	Redis Init
	"""
	def __init__(self, host='localhost', port=6379, db=0, password=None):
		self.redis_conn = redis.Redis(host=host, port=port, db=db, password=password)
 
	"""
	设置键值对，可以选择设置过期时间。
	"""
	def set_key(self, key, value, expire=None):
		if expire:
			return self.redis_conn.setex(key, expire, value)
		else:
			return self.redis_conn.set(key, value)
 
	"""
	获取键对应的值。
	"""
	def get_key(self, key):
		return self.redis_conn.get(key)
 
	"""
	删除一个键。
	"""
	def delete_key(self, key):
		return self.redis_conn.delete(key)
	
	"""
	获取Key的过期剩余时间
	"""
	def ttl(self, key):
		return self.redis_conn.ttl(key)

	"""
	"""
	def expire(self, key, expire=10):
		return self.redis_conn.expire(key, expire)

	"""
	更新一个键的值，可以选择更新过期时间。
	"""
	def update_key(self, key, value, expire=None):
		return self.set_key(key, value, expire)
 
	"""
	使用给定模式匹配键。
	"""
	def get_keys_by_pattern(self, pattern):
		return self.redis_conn.keys(pattern)

if __name__ == '__main__':
	pass 
	# 使用示例
	#redis_helper = RedisHelper('127.0.0.1', 444)
	# redis_helper.set_key('name', 'Alice')
	# print(redis_helper.get_key('name'))  # 输出: b'Alice'
	# redis_helper.delete_key('name')
	# print(redis_helper.get_key('name'))  # 输出: None

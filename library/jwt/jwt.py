# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.07.15

import jwt
import datetime
from library.util import util

"""
@brief JWT Encode Token
"""
def encode_token(uid = "", uname = ""):
	try:
		# JWT载荷部分
		payload = {
			"exp": datetime.datetime.utcnow() + datetime.timedelta(days = int(util.fetch_conf('global.ini', 'jwt', 'expire'))),
			"iat": datetime.datetime.utcnow(), # 开始时间
			"iss": "tornado",
			"payload": {
				"uid": uid,
				"uname": uname
			}   
		}

		auth_token = jwt.encode(payload, util.fetch_conf('global.ini', 'jwt', 'secret'), algorithm=util.fetch_conf('global.ini', 'jwt', 'algorithm'))
	except Exception as e:
		auth_token = e
	
	return auth_token

"""
@brief JWT Decode Token
"""
def decode_token(token):
	try:
		payload = jwt.decode(token, util.fetch_conf('global.ini', 'jwt', 'secret'), algorithms=[util.fetch_conf('global.ini', 'jwt', 'algorithm')])
		return payload
	except jwt.ExpiredSignatureError as e:
		return False
	except jwt.InvalidTokenError as e:
		return False

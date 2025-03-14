# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2025.02.19

import sys
import json
from library.util import util
from library.redis import redishelper
from controller.base import BaseHandler

class StrategyHandler():
    def __init__(self, uid = '9527', version = 'v1', cnf = 'global.ini'):
        self.uid = uid
        self.version = version
        host     = util.fetch_conf(cnf, 'redis', 'host')
        port     = util.fetch_conf(cnf, 'redis', 'port')
        db       = util.fetch_conf(cnf, 'redis', 'db')
        password = util.fetch_conf(cnf, 'redis', 'password')
        self.objRedis = redishelper.RedisHelper(host, port, db, password)
    
    """
	@brief 1 request interval X seconds
    """
    def sInterval(self, params):
        intervalKey = "interval_key_{}-{}".format(self.version, self.uid)
        intervalVal = self.objRedis.get_key(intervalKey)
        if intervalVal is not None:
            return {'code':400901, 'message':'limit s1', 'data':[]}
        else:
            self.objRedis.set_key(intervalKey, params.get('value', 's1'), params.get('interval', int(util.fetch_conf('global.ini', 'strategy', 'interval'))))
            return {'code':0, 'message':'success', 'data':[]}

    """
    @brief x request in X seconds
    """
    def sTimetotal(self, params):
        timetotalKey = "timetotal_key_{}-{}".format(self.version, self.uid)
        timetotalKeySon = "timetotal_key_son_{}-{}".format(self.version, self.uid)
        timetotalVal = self.objRedis.get_key(timetotalKey)
        if timetotalVal is not None:
            timetotalValSon = self.objRedis.get_key(timetotalVal)
            if timetotalValSon is None:
                self.objRedis.set_key(timetotalKeySon, 1, int(util.fetch_conf('global.ini', 'strategy', 'total_son_time')))
            else:
                if int(timetotalValSon) >= params.get('times', int(util.fetch_conf('global.ini', 'strategy', 'times'))):
                    return {'code':400902, 'message':'limit s2', 'data':[]}
                else:
                    self.objRedis.set_key(timetotalKeySon, int(timetotalValSon) + 1, int(util.fetch_conf('global.ini', 'strategy', 'total_son_time')))
            return {'code':0, 'message':'success', 'data':[]}
        else:
            self.objRedis.set_key(timetotalKey, timetotalKeySon, params.get('total', int(util.fetch_conf('global.ini', 'strategy', 'total_time'))))
            self.objRedis.set_key(timetotalKeySon, 1, int(util.fetch_conf('global.ini', 'strategy', 'total_son_time')))
            return {'code':0, 'message':'success', 'data':[]}

if __name__ == '__main__':
	pass

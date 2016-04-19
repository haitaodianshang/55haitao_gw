#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/18/16 5:22 PM
"""

#coding: utf8

from rpc_client import APIClient
from tornado.options import options

from security import appstore
from core import api_repository
from connection import get_connection

from socket import gethostname
import os
from hashlib import md5

from torndb import Connection, OperationalError

class TransactionConnection(Connection):
    def transaction(self, query, *parameters, **kwparameters):
        self._db.begin()
        cursor = self._cursor()
        status = True
        try:
            for sql in query:
                cursor.execute(sql, kwparameters or parameters)
            self._db.commit()
        except OperationalError, e:
            self._db.rollback()
            status = False
            raise Exception(e.args[1], e.args[0])
        finally:
            cursor.close()
        return status

class API_repository(object):
    def __init__(self):
        print 'init API_repository'


    def find(self, apipath):
        return api_repository.find(apipath)

class APP_repository(object):
    def __init__(self):
        print 'init APP_repository'

    def find(self, appid):
        return appstore.find_by_appid(appid)

class RPCContext(object):
    def __init__(self, app):
        """初始化rpc服务上下文
        """
        self.rpc_client = APIClient(options.register['ip'], options.register['port'])

        self.api_repo = API_repository()
        self.app_repo = APP_repository()
        self.host_name = gethostname()
        self.instance_id = md5("{}{}{}".format(self.host_name, options.port, os.getpid())).hexdigest()[:8]
        
        db = get_connection()
        
        from service.UserService import UserService
        from service.repository import UserRepo, DeviceRepo
        self.user_repo = UserRepo(db)
        self.device_repo = DeviceRepo(db)
        self.user_service = UserService(self.device_repo, self.user_repo)


#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/18/16 5:21 PM
"""

#coding: utf8
host = '0.0.0.0'
port = 8070         # TODO 服务端口号
instances = 1
register = {
    'ip': '127.0.0.1',  # TODO ETCD 地址
    'port': 2379,       # TODO ETCD 端口号
    'path': '/rpc',
    'timeout': 6 #心跳超时时间,超过该时间未汇报则为服务消失
}

contract_dir = './data'
appinfo_basedir = './data/app'

service_name = 'api_gate'

baijie_db = {
    'ip': '172.16.2.41',    # TODO 数据库地址
    'port': 3306,           # TODO 数据库端口号
    'user': '55haitao',     # TODO 数据库用户名
    'passwd': '55haitao',   # TODO 数据库密码
    'db': '55haitao_dev'    # TODO 数据库名
}

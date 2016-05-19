#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/18/16 5:22 PM
"""

host = '0.0.0.0'
port = 8070
instances = 1

register = {
    'ip': '127.0.0.1',
    'port': 2379,
    'path': '/rpc',
    'timeout': 6 #心跳超时时间,超过该时间未汇报则为服务消失
}

contract_dir = './data'
appinfo_basedir = './data/app'

service_name = 'api_gate'

baijie_db = {
    'ip': '10.168.100.78',
    'port': 3306,
    'user': 'root',
    'passwd': '55haitao',
    'db': '55haitao_test'
}

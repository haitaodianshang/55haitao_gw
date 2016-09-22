#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/18/16 5:21 PM
"""

#coding: utf8
host = '0.0.0.0'
port = 8070
instances = 1
register = {
    'ip': '172.16.2.41',
    'port': 2379,
    'path': '/rpc',
    'timeout': 6 #心跳超时时间,超过该时间未汇报则为服务消失
}

contract_dir = '/var/55haitao/gw_data'
appinfo_basedir = './data/55haitao/gw_data/app'

service_name = 'api_gate'

baijie_db = {
    'ip': '172.16.2.41',
    'port': 3306,
    'user': '55haitao',
    'passwd': '55haitao',
    'db': '55haitao_dev'
}

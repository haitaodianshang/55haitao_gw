#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/18/16 12:01 AM
"""

"""
api repository
"""
from tornado.options import options
from api_common import contract
import os, re

contract_store = {}
"""
{
    "groupname": {
        "methodname": {
        }
    }
}
"""

def load_by_contract(filename):
    global contract_store
    contract_doc = contract.load_contract(filename)
    if contract_doc['version'] != '0.0.1':
        raise Exception('unknown api contract version! {}'.format(filename))

    for group, groupdata in contract_doc['data']['groups'].items():
        if group not in contract_store:
            contract_store[group] = {}
        for info in groupdata:
            contract_store[group][info['api_name']] = info

def load(basedir):
    """加载所有的api package.json
    """

    re_filename = re.compile(r'\w*_\d+\.\d+\.\d+\.json')
    for filename in os.listdir(basedir):
        if re_filename.match(filename):
            load_by_contract(os.path.join(basedir, filename))

def find(api_path):
    """查找method_name
    """
    group, method_name = api_path.split('/')
    if group not in contract_store:
        return None

    group_data = contract_store[group]
    return group_data.get(method_name)

load(options.contract_dir)
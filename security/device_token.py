#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/18/16 12:07 AM
"""
import msgpack, time
from api_common.security import security
from base64 import b64decode

config = {}
def init(cfg):
    global config
    config = cfg

def issue_device_token(appid, device_id):
    # find userservice issue_device_token
    raise  NotImplemented('!!!')

def parse_token(aes_key, token):
    return security.decrypt_device_token(token, aes_key)

def validate_device_token(token, aes_key):
    token_data = parse_token(aes_key, token)
    if token_data:
        return {
            "token": token_data,
            "ttl": token_data['expire_time'] - int(time.time())
        }
    return None


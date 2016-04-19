#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/18/16 12:07 AM
"""
from api_common.security import security
from base64 import b64decode
import time

config = {}
def init(cfg):
    global config
    config = cfg

def issue_user_token(appid, user_id, device_id):
    # find userservice issue_device_token
    pass

def parse_token(aes_key, token):
    return security.decrypt_user_token(token, aes_key)

def validate_user_token(token, aes_key):
    token_data = parse_token(aes_key, token)
    if token_data:
        return {
            "token": token_data,
            "ttl": token_data['expire_time'] -  int(time.time())
        }
    return None


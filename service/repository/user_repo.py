#coding: utf8
import logging
from base_repo import BaseRepo

class UserRepo(BaseRepo):

    def check_user_login(self, appid, device_id, user_id):
        sql = ("SELECT user_token FROM 55haitao_user_token"
               "WHERE `appid`=%s AND `device_id`=%s AND `user_id`=%s AND `is_active`=1 ")
        tokens = self.db.query(sql, appid, device_id, user_id)
    
        if tokens and len(tokens) > 1:
            logging.error('find duplicate valid user token on same device')
            return tokens[0]['user_token']
        elif tokens and len(tokens) == 1:
            return tokens[0]['user_token']
        else:
            return None

#coding: utf8

class UserService(object):
    def __init__(self, device_repo, user_repo):
        self.device_repo = device_repo
        self.user_repo = user_repo

    def check_user_login(self, appid, device_id, user_id):
        """check user login info"""
        return self.user_repo.check_user_login(appid, device_id, user_id)
        

    
    

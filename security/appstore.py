#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/19/16 5:01 PM
"""

"""
appinfo storage
"""
import os, re, json
from tornado.options import options

appinfo_store = {

}

def load_appinfo(basedir):
    re_filename = re.compile(r'\d+\.json')
    for filename in os.listdir(basedir):
        if re_filename.match(filename):
            load_appinfo_by_file(os.path.join(basedir, filename))

def load_appinfo_by_file(filename):
    global appinfo_store
    with open(filename, 'r') as fp:
        appinfo = json.load(fp)
        appinfo_store[appinfo['appid']] = appinfo

def find_by_appid(appid):
    return appinfo_store.get(appid)

load_appinfo(options.appinfo_basedir)
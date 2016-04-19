#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/17/16 11:43 PM
"""

"""
基础错误码分段(-2000, -1)
"""
E_INPUT_PARSE_FAILED = -1 #
E_ARGUMENT_MISSING = -2 #参数缺失
E_INNER_ERROR = -3 #内部未知错误

E_METHOD_NEED       = -11 #_mt参数无法找到
E_METHOD_NOTFOUND   = -12 #_mt参数无法识别


E_APPID_UNREGISTED = -20 #appid没有注册


E_AUTH_DEVICE_ERROR =  -30 #device 解析失败
E_AUTH_DEVICE_EXPIRED =  -31 #device token 已经过期
E_AUTH_USERTOKEN_EXPIRED =  -41 #user token 已经过期
E_AUTH_USERTOKEN_ERROR = -40 #user token解析失败
E_AUTH_LOGIN_ON_OTHER_DEVICE = -42 #user已经在其他设备登陆

E_SIGN_UNKNOWN_SIGN_METHOD  = -50 #不支持的签名方法
E_SIGN_SIGN_ERROR           = -51 #签名错误

DOC={
    E_INPUT_PARSE_FAILED: '参数解析失败',
    E_METHOD_NEED: '_mt参数是必须参数',
    E_METHOD_NOTFOUND: '_mt参数无法识别',
    E_ARGUMENT_MISSING: '参数缺失'
}

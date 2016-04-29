#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/17/16 10:47 PM
"""

import json
import logging
import traceback, time

import tornado.gen
from tornado.web import RequestHandler

from api_common.constants import common_args_enum
from api_common.exception import CoreError, BizError
from api_exception import *
from core import constants as core_inst
from security import security_level, user_token, device_token
from security import data_integrity

logger = logging.getLogger("API")
access_logger = logging.getLogger('API.access')
rpc_audit_logger = logging.getLogger('RPC.audit')

class APIHandler(RequestHandler):
    def initialize(self):
        self.stat = {
            'systime': int(time.time()*1000),
            'cid': None
        }

    @property
    def context(self):
        return self.application.context

    def _generate_cid(self):
        """format: s:md5(host+port)[0:8],t:int(time.time())"""
        return "s:{}|t:{}".format(self.application.context.instance_id, int(time.time()*1000))

    def check_usertoken(self, user_token_data, token_str):
        #TODO: 互踢逻辑,根据同一user id在不同设备id登录状况
        token_in_db = self.context.user_service.check_user_login(user_token_data['token']['appid'],
                                                    user_token_data['token']['device_id'],
                                                    user_token_data['token']['user_id'])
        if token_in_db != token_str:
            raise CoreError(constants.E_AUTH_LOGIN_ON_OTHER_DEVICE, '该用户已经在其他设备登陆')

    def check_signature(self, se_level, data, dtk=None, tk=None):
        print data_integrity.sign(se_level, data, dtk=dtk, tk=tk), data.get('_sig'), data, se_level
        if data_integrity.sign(se_level, data, dtk=dtk, tk=tk) != data.get('_sig', None):
            raise CoreError(constants.E_SIGN_SIGN_ERROR, '不合法的签名')

    def options(self):
	
        self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin'))
        #self.set_header('Access-Control-Allow-Credentials', 'true')
        #self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.finish()

    @tornado.gen.coroutine
    def post(self):
        """接收post请求,并鉴权之后转发给各服务

        检查安全接口安全级别 -> 鉴权 -> 返回鉴权结果
        服务端接收请求处理顺序
        检查必须参数 _mt 是否完整
        """
        #self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin'))
	logging.info(self.request.headers.get('Origin'))
        try:
            input = json.loads(self.request.body)
            self.stat['cid'] = input.get('_cid') or self._generate_cid()
            access_logger.info("request_id: %s,  body:%s", self.stat['cid'], self.request.body)
        except Exception,e :
            logging.error('bad request:%s, exception:%s', self.request.body, traceback.format_exc())
            raise CoreError(core_inst.E_INPUT_PARSE_FAILED, core_inst.DOC[core_inst.E_INPUT_PARSE_FAILED])

        if '_mt' not in input:
            raise  CoreError(constants.E_METHOD_NEED, 'argument "_mt" missing')
        if '_sm' not in input:
            raise CoreError(constants.E_METHOD_NEED, 'argument "_sm" missing')


        api_info = self.context.api_repo.find(input['_mt'])
        if api_info is None:
            raise CoreError(constants.E_METHOD_NOTFOUND, 'unknown _mt:%s' % input['_mt'])

        if '_aid' not in input:
            raise MissingArgument('_aid')

        if api_info['se_level'] == security_level['UserLogin'] and '_tk' not in input:
            raise MissingArgument()

        elif api_info['se_level'] == security_level['DeviceLogin'] and '_tk' not in input and '_dtk' not in input:
            raise MissingArgument('_dtk')

        #校验签名
        if api_info['se_level'] not in [security_level['UserLogin'], security_level['DeviceLogin'], security_level['None']]:
            raise CoreError(constants.E_SIGN_UNKNOWN_SIGN_METHOD, '不支持的_sm参数')

        if input.get('_sm', '') != 'MD5':
            raise CoreError(constants.E_SIGN_UNKNOWN_SIGN_METHOD, '不支持的_sm参数')

        self.check_signature(api_info['se_level'], input, tk=input.get('_tk', None), dtk=input.get('_dtk', None))

        common_argument = {}
        app_info = self.context.app_repo.find(input['_aid'])
        if not app_info:
            raise BizError(constants.E_APPID_UNREGISTED, '未注册的appid')

        x_real_ip = self.request.headers.get("X-Real-IP")
        common_argument[common_args_enum.COMMON_ARGS_APP_ID.param] = input['_aid']
        common_argument[common_args_enum.COMMON_ARGS_CHANNEL.param] = input.get('_chl')
        common_argument[common_args_enum.COMMON_ARGS_VERSION.param] = input.get('_vc')
        common_argument[common_args_enum.COMMON_ARGS_CLIENT_IP.param] = x_real_ip or self.request.remote_ip
        common_argument[common_args_enum.COMMON_ARGS_CALL_ID.param] = self.stat['cid']
        common_argument[common_args_enum.COMMON_ARGS_PLATFORM.param] = input.get('_pl')

        user_token_data = None
        device_token_data = None
        if '_tk' in input and input.get('_tk') != None:
            try:
                logging.info('%s|%s', input['_tk'], app_info['usertoken_key'])
                user_token_data = user_token.validate_user_token(input['_tk'], app_info['usertoken_key'])

            except CoreError as ex:
                raise ex
            except Exception, e:
                logging.warn('decode user_token fail:%s', traceback.format_exc())
                pass
        if '_dtk' in input and input.get('_dtk') != None:
            try:
                device_token_data = device_token.validate_device_token(input['_dtk'], app_info['devicetoken_key'])
            except Exception, e:
                pass

        if api_info['se_level'] == security_level['UserLogin']:
            if not user_token_data:
                raise CoreError(constants.E_AUTH_USERTOKEN_ERROR, 'decode user_token fail')

            if user_token_data['ttl'] <= 0:
                raise CoreError(constants.E_AUTH_USERTOKEN_EXPIRED, 'user_token expired')

            common_argument[common_args_enum.COMMON_ARGS_USER_ID.param] = user_token_data['token']['user_id']
            common_argument[common_args_enum.COMMON_ARGS_DEVICE_ID.param] = user_token_data['token']['device_id']

        elif api_info['se_level'] == security_level['DeviceLogin']:
            if not device_token_data:
                raise CoreError(constants.E_AUTH_DEVICE_ERROR, 'decode device token fail')

            if device_token_data['ttl'] <= 0:
                raise CoreError(constants.E_AUTH_DEVICE_EXPIRED, 'device token expired!')

            common_argument[common_args_enum.COMMON_ARGS_USER_ID.param] = user_token_data['token'].get('user_id', 0) if user_token_data else 0
            common_argument[common_args_enum.COMMON_ARGS_DEVICE_ID.param] = device_token_data['token']['device_id']

            #设备登陆级别接口, 提供可用的_tk参数,依然可以注入user_id，否则注入默认参数
            if user_token_data:
                common_argument[common_args_enum.COMMON_ARGS_USER_ID.param] = user_token_data['token'].get('user_id', 0)

        elif api_info['se_level'] != security_level['None']:
            raise Exception('未知安全级别')

        if user_token_data:
            self.check_usertoken(user_token_data, input.get('_tk'))

        #TODO: 接收结果(结果retcode不为0则为异常,应该记录BizError或者CoreError,或者未知异常), 返回给客户端

        for param in api_info['rest_spec']['params']:
            if param['name'] == 'self': #跳过python self关键字
                continue
            elif 'inject_param' in param and param['inject_param']:
                if param['inject_param'].param not in common_argument:
                    input[param['name']] = param['default'] #如果没有注入成功则使用默认参数
                else:
                    input[param['name']] = common_argument[param['inject_param'].param]
        res = yield self.context.rpc_client(api_info['module_name'], api_info['api_name'], **input)
        rpc_audit_logger.info('{"module": "%s", "method": "%s", "call_time_ms": %d}',
                              api_info['module_name'], api_info['api_name'], int(time.time()*1000) - self.stat['systime'])
        res['stat'] = self.stat
        self.write(res)
        self.finish()


    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages."""
        #debug = self.settings.get("debug", False)
        try:
            exc_info = kwargs.pop('exc_info')
            e = exc_info[1]
            if isinstance(e, BizError):
                pass
            elif isinstance(e, CoreError):
                pass
            else:
                e = CoreError(500)

            exception = "".join([ln for ln in traceback.format_exception(*exc_info)])
            logger.error(exception)

            self.clear()
            self.set_status(200)  # always return 200 OK for API errors
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.finish({'code': e.code, 'data': e.data, 'msg': str(e)})
        except Exception:
            logging.error(traceback.format_exc())
            return super(APIHandler, self).write_error(status_code, **kwargs)

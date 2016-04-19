#coding: utf8

"""
@author: Wanzhi Du
@email : duwanzhi@55haitao.com
@time  : 2/17/16 11:37 PM
"""

"""
启动时读取api包发布文件, api包文件包含参数列表,接口注入需求, 安全级别

"""
#coding: utf8
import os, sys, logging
import platform, datetime
reload(sys)
sys.setdefaultencoding('utf-8')

if platform.system() == "Linux":
    os.environ["PYTHON_EGG_CACHE"] = "/tmp/egg"
_root = os.path.dirname(os.path.abspath(__file__))
# append tasks directory for celeryconfig.py
# sys.path.append(os.path.join(_root, "tasks"))
# chdir to current directory
# workaround for d3status-redis27 server which raise exception(celeryd use os.getcwd())
# when using supervisor to run app.py
os.chdir(_root)

from tornado import web, process
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.httpserver import HTTPServer
from tornado.options import options
from core.options import  parse_options
#from core import register
from core.APIHandler import APIHandler

class Application(web.Application):
    def __init__(self):
        settings = dict()
        # init etcd
        from context import RPCContext
        #self.etcd_client = register.init_etcd()
        self.context = RPCContext(self)

        super(Application, self).__init__([
            (r'^/m.api$', APIHandler)
        ], **settings)

    def reverse_api(self, request):
        """Returns a URL name for a request"""
        handlers = self._get_host_handlers(request)

        for spec in handlers:
            match = spec.regex.match(request.path)
            if match:
                return spec.name

        return None

def main():
    logging.basicConfig(format='[%(levelname)s %(asctime)s %(name)s %(module)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    parse_options()
    app = Application()
    http_server = HTTPServer(app, xheaders=True)
    http_server.bind(int(options.port), options.host)

    try:
        http_server.start(options.instances)
    except KeyboardInterrupt,e:
        logging.warn('parent exiting!')
        sys.exit(0)

    try:
        main_loop = IOLoop.instance()
        main_loop.start()
    except:
        logging.warn('child process exit! task_id: {}'.format(process.task_id()))

if __name__ == '__main__':
    main()

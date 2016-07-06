#coding: utf8
import torndb
from functools import wraps

__all__  = ['get_connection', 'transaction']

class Connection(torndb.Connection):

    def set_autocommit(self, flag):
        self._db.autocommit(flag)

    def commit(self):
        self._db.commit()

    def rollback(self):
        self._db.rollback()

class Transaction(object):

    def __enter__(self):
        self.conn = get_connection()
        self.conn.set_autocommit(False)

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn = get_connection()
        if exc_type :
            #OperationalError时数据库连接已关闭
            if exc_type is not torndb.OperationalError:
                self.conn.rollback()
            else:
                raise
        else:
            self.conn.commit()
        self.conn.set_autocommit(True)

    def __call__(self, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapped

def transaction():
    return Transaction()


_db_conn = None

def get_connection():
    global _db_conn
    if _db_conn is None:
        from tornado.options import options
        _db_conn = Connection('%s:%d' % (options.baijie_db['ip'],
                                         options.baijie_db['port']),
                              options.baijie_db['db'],
                              user=options.baijie_db['user'],
                              password=options.baijie_db['passwd'],
                              charset='utf8mb4', max_idle_time=100)
    return _db_conn

import redis
import inspect

class RedisPlugin(object):
    name = 'redis'

    def __init__(self,host='localhost',port=6379,database=0,keyword='rdb'):
      self.host = host
      self.port = port
      self.database = database
      self.keyword = keyword
      self.redisdb = None

    def setup(self,app):
        for other in app.plugins:
            if not isinstance(other,RedisPlugin): continue
            if other.keyword == self.keyword:
                raise PluginError("Found another redis plugin with "\
                        "conflicting settings (non-unique keyword).")

    def apply(self,callback,context):
        conf = context['config'].get('redis') or {}
        database = conf.get('rdb',self.database)
        host = conf.get('host',self.host)
        port = conf.get('port',self.port)
        keyword = conf.get('keyword',self.keyword)

        args = inspect.getargspec(context['callback'])[0]
        if keyword not in args:
            return callback

        if self.redisdb is None:
            self.redisdb = redis.ConnectionPool(host=host, port=port, db=database)

        def wrapper(*args,**kwargs):
            kwargs[self.keyword] = redis.Redis(connection_pool=self.redisdb)
            rv = callback(*args, **kwargs)
            return rv
        return wrapper

Plugin = RedisPlugin

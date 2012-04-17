import redis
import types

# Right now this is hard coded. Would be nice to have a util class that reads
# the ini file
HOST = 'localhost'
PORT = 6379

class MockRedis(object):
    """
    This class is a singleton that mocks the Redis API. Since this
    project uses such a limited feature set of redis, we've only mocked
    out the get/set functions. 
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """
        Override the new function of MockRedis to ensure you always
        get the same object. Mimicks a single long running process.
        """
        if not cls._instance:
            cls._instance = super(MockRedis, cls).__new__(cls, *args, **kwargs)
        
        return cls._instance
    
    def __init__(self):
        self.cache = { }
    
    def keys(self):
        return self.cache.keys()
    
    def delete(self, keys):
        # This should take a single value or a list
        # it simply clears all the keys for now if it's a list
        if isinstance(keys, types.StringTypes):
            del self.cache[keys]
        else:
            self.cache.clear()
    
    def get(self, key):
        return self.cache.get(key, '')
    
    def set(self, key, value):
        self.cache[key] = value

class Cache(object):
    env = 'prod'
    redis = None
    
    @staticmethod
    def clear_cache():
        # Clear all keys from the cache
        r = Cache.cache()
        r.flushdb()
    
    
    @staticmethod
    def cache():
        try:
            if not Cache.redis:
                Cache.redis = redis.StrictRedis(HOST, PORT, db=0)
                # Excercise redis to make sure we have a connection
                Cache.redis.set('__test__', '')
            
            return Cache.redis
        except:
            if Cache.env == 'prod':
                raise
            else:
                return MockRedis()
    
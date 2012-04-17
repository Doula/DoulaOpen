import json
from pprint import pprint as pretty_print
import re

def dirify(url):
    url = url.lower()
    url = url.replace('<', '')
    url = url.replace('>', '')
    url = url.replace('&', '')
    url = url.replace('"', '')
    url = re.sub(r'\s+', '_', url)
    url = re.sub(r'[^\d\w\s]!', '', url)
    
    return url


class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, object):
            return obj.__dict__
        
        raise TypeError(repr(obj) + " is not JSON serializable")
    

def dumps(obj):
    return ObjectEncoder().encode(obj)

def pprint(obj):
    pretty_print(dumps(obj))

def dirify(url):
    url = url.lower()
    url = url.replace('<', '')
    url = url.replace('>', '')
    url = url.replace('&', '')
    url = url.replace('"', '')
    url = re.sub(r'\s+', '_', url)
    url = re.sub(r'[^\d\w\s]!', '', url)
    
    return url

import json

class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, object):
            return obj.__dict__
        
        raise TypeError(repr(obj) + " is not JSON serializable")
    

def encode(obj):
    return ObjectEncoder().encode(obj)
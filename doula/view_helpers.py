import simplejson as json

def encode_complex(obj):
    if isinstance(obj, object):
        return obj.__dict__
    
    raise TypeError(repr(obj) + " is not JSON serializable")

def encode(obj):
    return json.JSONEncoder(default=encode_complex).encode(obj)

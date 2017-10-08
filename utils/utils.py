from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime
from uuid import uuid4
import os
import redis

class RedisSession:
    def __init__(self):
        self.manager = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=os.environ['REDIS_DB'], password=os.environ['REDIS_PASSWORD'])
        self.id = uuid4().__str__()

    def set_session_active(self):
        return self.manager.set("{}:active".format(self.id), True)

    def set_session_inactive(self):
        return self.manager.set("{}:active".format(self.id), False)

    @property
    def session_is_active(self):
        if self.manager.get("{}:active".format(self.id)).decode('iso-8859-1')) != "False":
            return True

        else:
            return False

    @property
    def get_obj_identifier(self):
        return self.id

    def __del__(self):
        self.manager.delete("{}:active".format(self.id))


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)

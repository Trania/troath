import os
import sys
from wsgiref.simple_server import make_server

from core.router import Router


base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base)


class Application(object):
    def __init__(self, router):
        self.router = router

    def __call__(self, env, start_response):
        return self.router.handle(env, start_response)

router = Router()
app = Application(router)
http = make_server('localhost', 8000, app)
http.serve_forever()
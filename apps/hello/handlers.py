from core.handlers import HTTPHandler, HTTPNotAllowedHandler
from core.decorators import template

class Hello(HTTPHandler):
    URL = '/'
    # TEMPLATE = 'hello.html'

    @template('hello.html')
    def get(self, req, res):
        return {'name':'Hamdy'}

    # def get(self, req, res):
    #     return 'helo'

    # def get(self, req, res):
    #     return HTTPNotAllowedHandler()
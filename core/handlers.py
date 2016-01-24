class HTTPError(object):
    def get(self, req, res):
        res.status = '405 Not Allowed'
        return 'Method Not Allowed'

    def post(self, req, res):
        res.status = '405 Not Allowed'
        return 'Method Not Allowed'

class HTTPNotAllowedHandler(HTTPError):
    pass

class HTTPHandler(HTTPNotAllowedHandler):
    pass
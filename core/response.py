class Response(object):
    def __init__(self):
        self.content_type = 'text/plain'
        self.content_length = 0

    status = '200 OK'

    @property
    def headers(self):
        return [
            ('Content-Type', self.content_type ),
            ('Content-Length', str(self.content_length))

        ]
    def write(self, content):
        self.start_response(self.status, self.headers)


class Request(object):
    def __init__(self, env):
        self._env = env
        self._params = None

    @property
    def params(self):
        if self._params is not None:
            return self._params
        self._params = {}
        for item in self._env['QUERY_STRING'].split('&'):
            k, v = item.split('=')
            self._params[k] = v
        return self._params





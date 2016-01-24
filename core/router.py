import pkgutil
import importlib
import inspect
import json
import os
import sys
from jinja2 import Template

import apps

from request import Request
from response import Response
from core.handlers import HTTPError


class Router(object):
    def __init__(self):
        self._templates = {}

    @property
    def handlers(self):
        if hasattr(self, '_handlers'):
            return self._handlers

        self._handlers = {}

        for importer, name, ispkg in pkgutil.iter_modules(apps.__path__):
            if not ispkg:
                continue
            try:
                handlers_mod = importlib.import_module('apps.%s.handlers' % name)
                app_path = os.path.dirname(os.path.abspath(handlers_mod.__file__))
                for item in dir(handlers_mod):
                    item = getattr(handlers_mod, item)
                    if not inspect.isclass(item):
                        continue
                    obj = item()
                    if hasattr(item, 'URL'):
                        params = {'GET':getattr(obj, 'get'),
                                  'POST': getattr(obj, 'post'),
                                  'TEMPLATE': getattr(obj, 'TEMPLATE', ''),
                                  'TEMPLATE_DIR':os.path.join(app_path, 'templates')
                                  }
                        self._handlers[item.URL.strip('/')] = params
            except ImportError:
               pass
        return self._handlers


    def get_template(self, path):
        if path not in self._templates:
            with open(path) as template:
                c = template.read()
                self._templates[path] = c
        return self._templates[path]

    def handle(self, env, start_response):
        url = env['PATH_INFO'].strip('/')
        method = env['REQUEST_METHOD']
        handler =  self.handlers.get(url)
        if handler:
            if method in handler:
                req = Request(env)
                res = Response()
                content = handler[method](req, res)
                template = handler['TEMPLATE']
                template_dir = handler['TEMPLATE_DIR']

                if isinstance(content, dict): #possibly wrapped by @template
                    if 'template' in content:
                        template = content['template']
                        content = content['content']

                if isinstance(content, HTTPError):
                    content = getattr(content, method.lower())(req, res)
                elif template and isinstance(content, dict):
                    template = os.path.join(template_dir, template)
                    content = str(Template(self.get_template(template)).render(content))
                    res.content_type = 'text/html'
                elif isinstance(content, dict):
                    content = json.dumps(content)
                    res.content_type = 'application/json'
                elif not content:
                    content = ''

                res.content_length = str(len(content))
                start_response(res.status, res.headers)
                return [content]


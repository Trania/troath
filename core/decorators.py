def template(name):
    def wrapper(func, *args, **kwargs):
        def inner(*args, **kwargs):
            content = func(*args, **kwargs)
            return {'content':content, 'template':name}
        return inner
    return wrapper
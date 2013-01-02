from unittest import TestCase as WebHelpersTestCase

def raises(exc, func, *args, **kw):
    try:
        func(*args, **kw)
    except exc:
        pass
    else:
        tup = func.__name__, e.__name__
        raise AssertionError("%s() did not raise %s" % tup)

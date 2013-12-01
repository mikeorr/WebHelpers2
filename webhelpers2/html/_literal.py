from __future__ import unicode_literals

import markupsafe
from markupsafe import escape_silent as escape

class literal(markupsafe.Markup):
    """Represents an HTML literal.
    
    This subclass of unicode has a ``.__html__()`` method that is 
    detected by the ``escape()`` function.
    
    Also, if you add another string to this string, the other string 
    will be quoted and you will get back another literal object.  Also
    ``literal(...) % obj`` will quote any value(s) from ``obj``.  If
    you do something like ``literal(...) + literal(...)``, neither
    string will be changed because ``escape(literal(...))`` doesn't
    change the original literal.

    Changed in WebHelpers 1.2: the implementation is now now a subclass of
    ``markupsafe.Markup``.  This brings some new methods: ``.escape`` (class
    method), ``.unescape``, and ``.striptags``.
    
    """
    __slots__ = ()

    def __new__(cls, base="", encoding=None, errors="strict"):
        if base is None:
            return EMPTY
        return super(literal, cls).__new__(cls, base, encoding, errors)

    @classmethod
    def escape(cls, s):
        if s is None:
            return EMPTY
        return super(literal, cls).escape(s)


EMPTY = literal("")

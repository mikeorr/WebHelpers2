from __future__ import unicode_literals

import markupsafe
from markupsafe import escape_silent as escape

class literal(markupsafe.Markup):
    """An HTML literal string, which will not be further escaped.

    I'm a subclass of ``markupsafe.Markup``, which itself is a subclass
    of ``unicode`` in Python 2 or ``str`` in Python 3. The main
    difference from ordinary strings is the ``.__html__`` method, which
    allows smart escapers to recognize it as a "safe" HTML string that
    doesn't need to be escaped.
    
    All my string methods preserve literal arguments and escape plain
    strings. However, in expressions you must pay attention to which
    value "controls" the expression. I seem to be able to control all
    combinations of the ``+`` operator, but with ``%`` and ``.join`` I
    must be on the left side. So these all work::

        "A" + literal("B")
        literal(", ".join(["A", literal("B")])
        literal("%s %s") % (16, literal("kg"))

    But these return plain strings which are vulnerable to
    double-escaping later::

        "\\n".join([literal("<span>A</span"), literal("Bar!")])
        "%s %s" % ([literal("16"), literal("&lt;&gt;")])
    """
    __slots__ = ()

    def __new__(cls, base="", encoding=None, errors="strict"):
        """Constructor.

        I convert my first argument to a string like ``str()`` does.
        However, I convert ``None`` to the empty string, which is
        usually what's desired in templates. (In contrast, raw
        ``Markup(None)`` returns ``"None"``.)

        Examples::

            >>> literal("A")   # => literal("A")
            >>> literal(">")   # => literal(">")
            >>> literal(None)  # => literal("")
            >>> literal(11)    # => literal("11")
            >>> literal(datetime.date.today())   # => literal("2014-08-31")

        The default encoding is "ascii".
        """
        if base is None:
            return EMPTY
        return super(literal, cls).__new__(cls, base, encoding, errors)

    @classmethod
    def escape(cls, s):
        """Escape the argument and return a literal.

        This is a *class* method. The result depends on the argument type:

        * literal: return unchanged.
        * an object with an ``.__html__`` method: call it and
          return the result. The method should take no arguments and
          return the object's preferred HTML representation as a string.
        * plain string: escape any HTML markup characters in it, and
          wrap the result in a literal to prevent double-escaping later.
        * non-string: call ``str()``, escape the result, and wrap it in
          a literal.
        * None: convert to the empty string and return a literal.

        If the argument has an ``.__html__`` method, I call it and
        return the result. This causes literals to pass through unchanged,
        and other objects with an ``.__html__`` method return their
        preferred HTML representation. If the argument is a plain
        string, I escape any HTML markup characters and wrap the result
        in a literal to prevent further escaping. If the argument is a
        non-string, I convert it to a string, escape it, and wrap it in
        a literal.  Examples::

            >>> literal.escape(">")            # => literal("&gt;")
            >>> literal.escape(literal(">"))   # => literal(">")
            >>> literal.escape(None)           # => literal("")

        I call ``markupsafe.escape_silent()``. It escapes double quotes
        as "&#34;", single quotes as "&#39;", "<" as "&lt;", ">" as
        "&gt;", and "&" as "&amp;".
        """
        if s is None:
            return EMPTY
        return super(literal, cls).escape(s)

    def lit_join(self, iterable):
        """Like ``self.join`` but don't escape elements in the iterable."""
        s = super(markupsafe.Markup, self).join(iterable)
        return self.__class__(s)


EMPTY = literal("")

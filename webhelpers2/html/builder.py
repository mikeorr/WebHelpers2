"""HTML/XHTML tag builder

HTML Builder provides: 

* an ``HTML`` object that creates (X)HTML tags in a Pythonic way.  

* a ``literal`` class used to mark strings containing intentional HTML markup. 

* a smart ``escape()`` function that preserves literals but
  escapes other strings that may accidentally contain markup characters ("<",
  ">", "&", '"', "'") or malicious Javascript tags.  Escaped strings are
  returned as literals to prevent them from being double-escaped later.

``literal`` is a subclass of ``unicode``, so it works with all string methods
and expressions.  The only thing special about it is the ``.__html__`` method,
which returns the string itself.  The ``escape()`` function follows a simple
protocol: if the object has an ``.__html__`` method, it calls that rather than
``.__str__`` to get the HTML representation.  Third-party libraries that do not
want to import ``literal`` (and this create a dependency on WebHelpers) can put
an ``.__html__`` method in their own classes returning the desired HTML
representation.

WebHelpers 1.2 uses MarkupSafe, a package which provides an enhanced
implementation of this protocol. Mako and Pylons have also switched to
MarkupSafe. Its advantages are a C speedup for escaping,
escaping single-quotes for security, and adding new methods to
``literal``. **literal** is now a subclass of ``markupsafe.Markup``.
**escape** is ``markupsafe.escape_silent``. (The latter does not exist yet in
MarkupSafe 0.9.3, but WebHelpers itself converts None to "" in the meantime). 

Single-quote escaping affects HTML attributes that are written like this:
*alt='Some text.'* rather than the normal *alt="Some text."*  If the text is a
replaceable parameter whose value contains a single quote, the browser would
think the value ends earlier than it does, thus enabling a potential cross-site
scripting (XSS) attack. WebHelpers 1.0 and earlier escaped double quotes but
not single quotes. MarkupSafe escapes both double and single quotes, preventing
this sort of attack.

MarkupSafe has some slight differences which should not cause compatibility
issues but may in the following edge cases.  (A) The ``force`` argument to
``escape()`` is gone. We doubt it was ever used. (B) The default encoding of
``literal()`` is "ascii" instead of "utf-8". (C) Double quotes are escaped as
"&#34;" instead of "&quot;". Single quotes are escaped as "&#39;". 

When ``literal`` is used in a mixed expression containing both literals and
ordinary strings, it tries hard to escape the strings and return a literal.
However, this depends on which value has "control" of the expression.
``literal`` seems to be able to take control with all combinations of the ``+``
operator, but with ``%`` and ``join`` it must be on the left side of the
expression.  So these all work::

    "A" + literal("B")
    literal(", ").join(["A", literal("B")])
    literal("%s %s") % (16, literal("kg"))

But these return an ordinary string which is prone to double-escaping later::

    "\\n".join([literal('<span class="foo">Foo!</span>'), literal('Bar!')])
    "%s %s" % (literal("16"), literal("&lt;em&gt;kg&lt;/em&gt;"))

Third-party libraries that don't want to import ``literal`` and thus avoid a
dependency on WebHelpers can add an ``.__html__`` method to any class, which
can return the same as ``.__str__`` or something else.  ``escape()`` trusts the
HTML method and does not escape the return value.  So only strings that lack
an ``.__html__`` method will be escaped.

The ``HTML`` object has the following methods for tag building:

``HTML(*strings)``
    Escape the string args, concatenate them, and return a literal.  This is
    the same as ``escape(s)`` but accepts multiple strings.  Multiple args are
    useful when mixing child tags with text, such as::

        html = HTML("The king is a >>", HTML.strong("fink"), "<<!")

``HTML.literal(*strings)``
    Same as ``literal`` but concatenates multiple arguments.

``HTML.comment(*strings)``
    Escape and concatenate the strings, and wrap the result in an HTML 
    comment.

``HTML.tag(tag, *content, **attrs)``
    Create an HTML tag ``tag`` with the keyword args converted to attributes.
    The other positional args become the content for the tag, and are escaped
    and concatenated.  If an attribute name ends in an underscore, remove it
    (e.g., "class\_" -> "class"). All other underscores in attribute names are
    converted to hyphens ("data_foo" -> "data-foo").  If an attribute value is
    ``None``, the attribute is not inserted.  Two special keyword args are
    recognized:
    
    ``c``
        Specifies the content.  This cannot be combined with content in
        positional args.  The purpose of this argument is to position the
        content at the end of the argument list to match the native HTML
        syntax more closely.  Its use is entirely optional.  The value can
        be a string, a tuple, or a tag.

    ``_closed``
        If present and false, do not close the tag.  Otherwise the tag will be
        closed with a closing tag or an XHTML-style trailing slash as described
        below.

    ``_nl``
        If present and true, insert a newline before the first content
        element, between each content element, and at the end of the tag.

    Example:

    >>> HTML.tag("a", href="http://www.yahoo.com", name=None, 
    ... c="Click Here")
    literal(u'<a href="http://www.yahoo.com">Click Here</a>')


``HTML.__getattr__``
    Same as ``HTML.tag`` but using attribute access.  Example:

    >>> HTML.a("Foo", href="http://example.com/", class_="important")
    literal(u'<a class="important" href="http://example.com/">Foo</a>')

``HTML.cdata``
    Wrap the text in a "<![CDATA[ ... ]]>" section. Plain strings will not be
    escaped because CDATA itself is an escaping syntax.

    >>> HTML.cdata(u"Foo")
    literal(u'<![CDATA[Foo]]>')

    >>> HTML.cdata(u"<p>")
    literal(u'<![CDATA[<p>]]>')

About XHTML and HTML
--------------------

This builder always produces tags that are valid as *both* HTML and XHTML.
"Void" tags -- those which can never have content like ``<br>`` and ``<input>``
-- are written like ``<br />``, with a space and a trailing ``/``.

*Only* void tags get this treatment.  The library will never, for
example, produce ``<script src="..." />``, which is invalid HTML.  Instead
it will produce ``<script src="..."></script>``.

The `W3C HTML validator <http://validator.w3.org/>`_ validates these
constructs as valid HTML Strict.  It does produce warnings, but those
warnings warn about the ambiguity if this same XML-style self-closing
tags are used for HTML elements that are allowed to take content (``<script>``,
``<textarea>``, etc).  This library never produces markup like that.

Rather than add options to generate different kinds of behavior, we
felt it was better to create markup that could be used in different
contexts without any real problems and without the overhead of passing
options around or maintaining different contexts, where you'd have to
keep track of whether markup is being rendered in an HTML or XHTML
context.

If you _really_ want tags without training slashes (e.g., ``<br>`)`, you can
abuse ``_closed=False`` to produce them.

"""

from __future__ import unicode_literals
import collections
import functools
import re

from six.moves.urllib.parse import quote as url_escape

# Literal imports and constants
from ._literal import literal, EMPTY
escape = literal.escape
NL = literal("\n")
BR = literal("<br />")

__all__ = ["HTML", "escape", "literal", "url_escape", "lit_sub"]

# Not included in __all__ because for specialized purposes only: 
# "format_attrs".


class HTMLBuilder(object):
    
    """Base HTML object."""
    
    literal = literal

    void_tags = {
        "area",
        "base",
        "basefont",
        "br",
        "col",
        "frame",
        "hr",
        "img",
        "input",
        "isindex",
        "link",
        "meta",
        "param",
        }
    boolean_attrs = {
        "defer",
        "disabled",
        "multiple",
        "readonly",
        }
    compose_attrs = {
        "class": literal(" "),
        "style": literal("; "),
        }

    # Opening and closing syntax for special HTML constructs.
    _cdata_tag = literal("<![CDATA["), literal("]]>")
    _comment_tag = literal("<!-- "), literal(" -->")

    def __call__(self, *args, **kw):
        """Join raw HTML and HTML escape it."""
        nl = kw.pop("nl", False)
        lit = kw.pop("lit", False)
        if kw:
            raise TypeError("unknown keyword args: {}".format(sort(kw)))
        if not lit:
            args = map(escape, args)
        if nl:
            ret = NL.lit_join(args) + NL
        else:
            ret = EMPTY.lit_join(args)
        return ret

    def tag(self, tag, *args, **kw):
        if "c" in kw:
            assert not args, "The special 'c' keyword argument cannot be used "\
    "in conjunction with non-keyword arguments"
            args = kw.pop("c")
        closed = kw.pop("_closed", True)
        nl = kw.pop("_nl", False)
        attrs = kw
        self.optimize_attrs(attrs)
        attrs_str = format_attrs(**attrs)
        if not args and tag in self.void_tags and closed:
            substr = '<%s%s />'
            html = literal(substr % (tag, attrs_str))
        else:
            chunks = ["<%s%s>" % (tag, attrs_str)]
            chunks.extend(escape(x) for x in args)
            if closed:
                chunks.append("</%s>" % tag)
            if nl:
                html = "\n".join(chunks)
            else:
                html = "".join(chunks)
        if nl:
            html += "\n"
        return literal(html)

    def __getattr__(self, attr):
        """Generate the tag for the given attribute name."""
        if attr.startswith('_'):
            raise AttributeError(attr)
        tag = functools.partial(self.tag, attr.lower())
        self.__dict__[attr] = tag
        return tag

    def comment(self, *args):
        parts = [self._comment_tag[0]]
        parts.extend(args)
        parts.append(self._comment_tag[1])
        return self(*parts)

    def cdata(self, *args): 
        """Wrap the content in a "<![CDATA[ ... ]]>" section.

        The content will not be escaped because CDATA itself is an 
        escaping syntax.
        """
        parts = [self._cdata_tag[0]]
        parts.extend(args)
        parts.append(self._cdata_tag[1])
        return self(*parts, lit=True)

    # Private methods
    def optimize_attrs(self, attrs):
        """Perform various transformations on an HTML attributes dict.

        Modifies 'attrs' in place.
        """
        if "class_" in attrs:
            attrs["class"] = attrs.pop("class_")
        for at in self.compose_attrs:
            value = attrs.get(at)
            if isinstance(value, (list, tuple)):
                if value:
                    sep = self.compose_attrs[at]
                    attrs[at] = sep.join(value)
                else:
                    del attrs[at]

def _attr_decode(v):
    """Parse out attributes that begin with '_'."""
    if v.endswith('_'):
        v = v[:-1]
    v = v.replace("_", "-")
    return v


def format_attrs(**attrs):
    """Format HTML attributes into a string of ' key="value"' pairs which
    can be inserted into an HTML tag.

    The attributes are sorted alphabetically.  If any value is None, the entire
    attribute is suppressed.

    Usage:
    >>> format_attrs(p=2, q=3)
    literal(u' p="2" q="3"')
    >>> format_attrs(p=2, q=None)
    literal(u' p="2"')
    >>> format_attrs(p=None)
    literal(u'')
    """
    strings = [' %s="%s"' % (_attr_decode(attr), escape(value))
        for attr, value in sorted(attrs.items())
        if value is not None]
    return literal("".join(strings))


def lit_sub(*args, **kw):
    """Literal-safe version of re.sub.  If the string to be operated on is
    a literal, return a literal result.  All arguments are passed directly to
    ``re.sub``.
    """
    lit = hasattr(args[2], '__html__')
    cls = args[2].__class__
    result = re.sub(*args, **kw)
    if lit:
        return cls(result)
    else:
        return result


HTML = HTMLBuilder()

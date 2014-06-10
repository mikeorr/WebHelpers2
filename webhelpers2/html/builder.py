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


``HTML.__getattr__``
    Same as ``HTML.tag`` but using attribute access.  Example:

    >>> HTML.a("Foo", href="http://example.com/", class_="important")
    literal(u'<a class="important" href="http://example.com/">Foo</a>')

``HTML.cdata``
    Wrap the text in a "<![CDATA[ ... ]]>" section. Plain strings will not be
    escaped because CDATA itself is an escaping syntax. ::

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

import six
from six.moves.urllib.parse import quote as url_escape

# Literal imports and constants
from ._literal import literal, EMPTY
escape = literal.escape
NL = literal("\n")
BR = literal("<br />\n")

__all__ = ["HTML", "escape", "literal", "url_escape", "lit_sub"]


class HTMLBuilder(object):
    
    """Base HTML object."""
    
    literal = literal

    EMPTY = EMPTY
    SPACE = literal(" ")
    TAB2 = literal("  ")
    TAB4 = literal("    ")
    NL = NL
    BR = BR
    NL2 = NL * 2
    BR2 = BR * 2

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
        boolean_attrs = kw.pop("_bool", None)
        attrs = kw
        self.optimize_attrs(attrs, boolean_attrs)
        attrs_str = self.render_attrs(attrs)
        chunks = []
        if not args and tag in self.void_tags and closed:
            substr = literal("<{}{} />")
            html = substr.format(tag, attrs_str)
            chunks.append(html)
        else:
            substr = literal("<{}{}>")
            html = substr.format(tag, attrs_str)
            chunks.append(html)
            chunks.extend(args)
            if closed:
                substr = literal("</{}>")
                chunks.append(substr.format(tag))
        return self(*chunks, nl=nl)

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
    def optimize_attrs(self, attrs, boolean_attrs=None):
        """Perform various transformations on an HTML attributes dict.

        Arguments:

        * **attrs**: the attribute dict. Modified in place!
        * **boolean_attrs**: set of attribute names to consider
          boolean in addition to ``self.boolean_attrs``.

        Modifies 'attrs' in place. Actions:

        1. Delete keys whose value is None.
        2. Delete trailing underscores in keys.
        3. Replace non-trailing underscores with hyphens.
        4. If a key is listed in 'self.compose_attrs' and the value is
           a list or tuple, join the elements into a string using the separator
           specified. If the value is an empty list/tuple, delete the key
           entirely. If any element is itself a 2-tuple, the first subelement is
           the string item, and the second is treated as a boolean flag.  If
           the flag is true, keep the item, otherwise delete it from the list.
           This allows users to programatically set the parts of a composeable
           attribute in a template without extra loops and logic code.
        5. For the 'class' attribute (or 'class_'), if the value is a
           list/tuple and any elements are 2-tuples, treat the second
           subelement
        6. If a key is listed in 'self.boolean_attrs' or the 'boolean_attrs'
           argument, convert the value to an HTML boolean. If the value is
           true, set the value to match the key. If the value is false, 
           delete the key.
        """
        if boolean_attrs:
            boolean_keys = self.boolean_attrs.union(boolean_attrs)
        else:
            boolean_keys = self.boolean_attrs
        # Make a copy of the keys because we'll be adding/deleting in the
        # original dict.
        keys = list(attrs.keys()) if six.PY3 else attrs.keys()
        for key in keys:
            value = attrs[key]
            is_seq = isinstance(value, (list, tuple))
            # Delete key if None value.
            if value is None:
                del attrs[key]
                continue
            # Rename key if it contains internal or trailing underscores.
            key_orig = key
            while key.endswith("_"):
                key = key[:-1]
            key = key.replace("_", "-")
            if key != key_orig:
                attrs[key] = attrs.pop(key_orig)
            # Convert "composeable attributes" from list to delimited string.
            if key in self.compose_attrs and isinstance(value, (list, tuple)):
                # Convert 2-tuples to regular elements.
                value_orig = value
                value = []
                for elm in value_orig:
                    if isinstance(elm, (list, tuple)) and len(elm) == 2:
                        if elm[1]:
                            value.append(elm[0])
                        # Else ignore the element.
                    else:
                        value.append(elm)
                # If value is non-empty, join the elements. If empty, delete
                # the key.
                if value:
                    sep = self.compose_attrs[key]
                    attrs[key] = sep.join(value)
                else:
                    del attrs[key]
            # Convert boolean attributes.
            if key in boolean_keys:
                if value:
                    attrs[key] = key   # Set the value to match the key.
                else:
                    del attrs[key]
            key_orig = value_orig = None  # To guard against bugs.

    def render_attrs(self, attrs):
        """Format HTML attributes into a string of ' key="value"' pairs which
        can be inserted into an HTML tag.
        """
        keys = sorted(attrs)
        fmt = literal(' {}="{}"')
        strings = [fmt.format(x, attrs[x]) for x in keys]
        return EMPTY.join(strings)


def lit_sub(*args, **kw):
    """Literal-safe version of re.sub.  If the string to be operated on is
    a literal, return a literal result.  All arguments are passed directly to
    ``re.sub``.
    """
    lit = hasattr(args[2], '__html__')
    cls = args[2].__class__
    result = re.sub(*(six.text_type(arg) if hasattr(arg,'__html__') else arg for arg in args), **kw)
    if lit:
        return cls(result)
    else:
        return result


HTML = HTMLBuilder()

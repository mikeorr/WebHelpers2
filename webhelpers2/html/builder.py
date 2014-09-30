"""HTML/XHTML/HTML 5 tag builder.
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
    
    """An HTML tag generator."""
    
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

        """Escape the string args, concatenate them, and return a literal.

        This is the same as ``literal.escape(s)`` but accepts multiple
        strings.  Multiple arguments are useful when mixing child tags
        with text, such as::

            html = HTML("The king is a >>", HTML.strong("fink"), "<<!")

        Keyword args:

        ``nl``
            If true, append a newline to the value. (Default False.)

        ``lit``
            If true, don't escape the arguments. (Default False.)
        """

        nl = kw.pop("nl", False)
        lit = kw.pop("lit", False)
        if kw:
            raise TypeError("unknown keyword args: {}".format(sorted(kw)))
        if not lit:
            args = map(escape, args)
        if nl:
            ret = NL.lit_join(args) + NL
        else:
            ret = EMPTY.lit_join(args)
        return ret

    def tag(self, tag, *args, **kw):

        """Create an HTML tag.

        ``tag`` is the tag name. The other positional arguments become the
        content for the tag, and are escaped and concatenated.

        Keyword arguments are converted to HTML attributes, except for
        the following special arguments:

        ``c``
            Specifies the content.  This cannot be combined with content
            in positional args.  The purpose of this argument is to
            position the content at the end of the argument list to
            match the native HTML syntax more closely.  Its use is
            entirely optional.  The value can be a string, a tuple, or a
            tag.

        ``_closed``
            If present and false, do not close the tag.  Otherwise the
            tag will be closed with a closing tag or an XHTML-style
            trailing slash.

        ``_nl``
            If present and true, insert a newline before the first content
            element, between each content element, and at the end of the tag.

            Note that this argument has a leading underscore while the
            same argument to ``__call__`` doesn't. That's because
            this method has so many other complex arguments, and for
            backward compatibility.

        ``_bool``
            Additional HTML attributes to consider boolean beyond those
            listed in ``.boolean_attrs``. See "Class Attributes" below.


        Other keyword arguments are converted to HTML attributes after
        undergoing several transformations:

        * Ignore attributes whose value is None.

        * Delete trailing underscores in attribute names. 
          ('class\_' -> 'class').

        * Replace non-trailing underscores with hyphens. ('data_foo' ->
          'data-foo').

        * If the attribute is "defer", "disable", "multiple", or
          "readonly", render it as an HTML 5 boolean attribute. If the
          value is true, copy the attribute name to the value. If the
          value is false, don't render the attribute at all.
          See ``self.boolean_attrs`` and ``_bool`` to customize which
          attributes are considered boolean.

        * If the attribute is "class" or "class\_" and the value is a
          list or tuple, convert the value to a space-delimited string.
          If the value is an empty list/tuple, don't render the
          attribute at all. If the value contains elements that are
          2-tuples, the first subelement is the string item, and the
          second subelement is a boolean flag; render only subelements
          whose flag is true.  This allows users to programatically set
          the parts of a composable attribute in a template without
          extra loops or logic code.

        * Likewise for "style", if the value is a list/tuple, convert it
          to a semicolon-delimited string, with a space after the
          semicolon. See ``self.compose_attrs`` to customize which
          attributes have list/tuple conversion and what their delimiter
          is.

        Examples:

        >>> HTML.tag("div", "Foo", class_="important")
        literal(u'<div class="important">Foo</div>')
        >>> HTML.tag("div", "Foo", class_=None)
        literal(u'<div>Foo</div>')
        >>> HTML.tag("div", "Foo", class_=["a", "b"])
        literal(u'<div class="a b">Foo</div>')
        >>> HTML.tag("div", "Foo", class_=[("a", False), ("b", True)])
        literal(u'<div class="b">Foo</div>')
        >>> HTML.tag("div", "Foo", style=["color:black", "border:solid"])
        literal(u'<div style="color:black; border:solid">Foo</div>')
        >>> HTML.tag("br")
        literal(u'<br />')
        >>> HTML.tag("input", disabled=True)
        literal(u'<input disabled="disabled"></input>')
        >>> HTML.tag("input", disabled=False)
        literal(u'<input></input>')

        To generate opening and closing tags in isolation:

        >>> HTML.tag("div", _closed=False)
        literal(u'<div>')
        >>> HTML.tag("/div", _closed=False)
        literal(u'</div>')
        """

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

        """Same as the ``tag`` method but using attribue access.

        ``HTML.a(...)`` is equivalent to ``HTML.tag("a", ...)``.
        """

        if attr.startswith('_'):
            raise AttributeError(attr)
        tag = functools.partial(self.tag, attr.lower())
        self.__dict__[attr] = tag
        return tag

    def comment(self, *args):

        """Wrap the content in an HTML comment.

        Escape and concatenate the string arguments.

        Example:

        >>> HTML.comment("foo", "bar")
        literal(u'<!-- foobar -->')
        """

        parts = [self._comment_tag[0]]
        parts.extend(args)
        parts.append(self._comment_tag[1])
        return self(*parts)

    def cdata(self, *args): 

        """Wrap the content in a "<![CDATA[ ... ]]>" section.

        Plain strings will not be escaped because CDATA itself is an
        escaping syntax. Concatenate the arguments:

        >>> HTML.cdata(u"Foo")
        literal(u'<![CDATA[Foo]]>')

        >>> HTML.cdata(u"<p>")
        literal(u'<![CDATA[<p>]]>')
        """

        parts = [self._cdata_tag[0]]
        parts.extend(args)
        parts.append(self._cdata_tag[1])
        return self(*parts, lit=True)

    def render_attrs(self, attrs):

        """Format HTML attributes into a string of ' key="value"' pairs.

        You don't normally need to call this because the ``tag`` method
        calls it for you. However, it can be useful for lower-level
        formatting in string templates like this:

        .. code-block:: mako

           Click <a href="http://example.com/"{attrs1}>here</a>
           or maybe <a{attrs2}>here</a>.


        ``attrs`` is a list of attributes. The values will be escaped if
        they're not literals, but no other transformation will be
        performed on them.

        The return value will have a leading space if any attributes are
        present. If no attributes are specified, the return value is the
        empty string literal. This allows it to render prettily in
        the interpolations above regardless of whether ``attrs``
        contains anything.
        """

        keys = sorted(attrs)
        fmt = literal(' {}="{}"')
        strings = [fmt.format(x, attrs[x]) for x in keys]
        return EMPTY.join(strings)

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
        3. Replace non-trailing underscores in keys with hyphens.
        4. If a key is listed in 'self.compose_attrs' and the value is
           a list or tuple, join the elements into a string using the separator
           specified. If the value is an empty list/tuple, delete the key
           entirely. If any element is itself a 2-tuple, the first subelement is
           the string item, and the second is treated as a boolean flag.  If
           the flag is true, keep the item, otherwise delete it from the list.
           This allows users to programatically set the parts of a composeable
           attribute in a template without extra loops and logic code.
        5. If a key is listed in 'self.boolean_attrs' or the 'boolean_attrs'
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


def lit_sub(*args, **kw):
    """Literal-safe version of re.sub.  If the string to be operated on is
    a literal, return a literal result.  All arguments are passed directly to
    ``re.sub``.
    """
    pattern = args[0]
    repl = args[1]
    string = args[2]
    extra = args[3:]
    lit = hasattr(args[2], '__html__')
    cls = args[2].__class__
    if six.PY3:
        # ``re.sub`` overescapes if the third arg is a literal in Python 3.
        string = str(string)
    result = re.sub(pattern, repl, string, *extra, **kw)
    if lit:
        return cls(result)
    else:
        return result


HTML = HTMLBuilder()

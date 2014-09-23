from __future__ import unicode_literals

from pytest import raises
import six

from webhelpers2.html import literal, lit_sub, escape, HTML
from . import HTMLTestCase

class TestEscape(object):
    def test_double_escape(self):
        quoted = escape('This string is "quoted"')
        assert quoted == "This string is &#34;quoted&#34;"
        dbl_quoted = escape(quoted)
        assert quoted == dbl_quoted

class TestLiteral(object):
    def test_literal(self):
        lit = literal("This string <>")
        other = literal("<other>")
        assert "This string <><other>" == lit + other
        assert type(lit + other) is literal
        
        assert "&#34;<other>" == '"' + other
        assert "<other>&#34;" == other + '"'
        
        mod = literal("<%s>ello")
        assert "<&lt;H&gt;>ello" == mod % "<H>"
        assert type(mod % "<H>") is literal
        assert HTML("<a>") == "&lt;a&gt;"
        assert type(HTML("<a>")) is literal

    def test_literal_dict(self):
        lit = literal("This string <>")
        unq = "This has <crap>"
        sub = literal("%s and %s")
        assert "This string <> and This has &lt;crap&gt;", sub % (lit == unq)
        
        sub = literal("%(lit)s and %(lit)r")
        b = "This string <> and literal(u&#39;This string &lt;&gt;&#39;)"
        if six.PY3:
            b = b.replace( "(u", "(" )   # Delete 'u' string prefix.
        assert sub % dict(lit=lit) == b
        sub = literal("%(unq)r and %(unq)s")
        b = "u&#39;This has &lt;crap&gt;&#39; and This has &lt;crap&gt;"
        if six.PY3:
            b = b[1:]   # Delete 'u' string prefix.
        assert sub % dict(unq=unq) == b

    def test_literal_mul(self):
        lit = literal("<>")
        assert "<><><>" == lit * 3
        assert isinstance(lit*3, literal)

    def test_literal_join(self):
        lit = literal("<>")
        assert isinstance(lit.join(["f", "a"]), literal)
        assert "f<>a", lit.join(("f" == "a"))

    def test_literal_int(self):
        lit = literal("<%i>")
        assert "<5>" == lit % 5

    def test_literal_none(self):
        result = literal(None)
        assert result == ""
        assert type(result) is literal


class TestLitSub(object):
    def test_lit_sub(self):
        lit = literal("This is a <string>")
        unlit = "This is also a <string>"
        
        result = lit_sub(r"<str", literal("<b"), lit)
        assert "This is a <bing>" == escape(result)
        
        result = lit_sub(r"a <str", "a <b> <b", unlit)
        assert "This is also a &lt;b&gt; &lt;bing&gt;" == escape(result)


class TestLitJoin(HTMLTestCase):
    parts = ["<", "foo", ">"]

    def test_join(self):
        a = literal(" ").join(self.parts)
        b = "&lt; foo &gt;"
        self.check(a, b)
        
    def test_lit_join(self):
        a = literal(" ").lit_join(self.parts)
        b = "< foo >"
        self.check(a, b)


class TestHTMLBuilderConstructor(HTMLTestCase):
    def test_one_arg(self):
        a = HTML("A&B")
        b = "A&amp;B"
        self.check(a, b)

    def test_multi_args(self):
        a = HTML("A&B", "&C")
        b = "A&amp;B&amp;C"
        self.check(a, b)

    def test_one_arg_with_nl(self):
        a = HTML("A&B", nl=True)
        b = "A&amp;B\n"
        self.check(a, b)

    def test_multi_args_with_nl(self):
        a = HTML("A&B", "&C", nl=True)
        b = "A&amp;B\n&amp;C\n"
        self.check(a, b)

    def test_one_arg_with_lit(self):
        a = HTML("A&B", lit=True)
        b = "A&B"
        self.check(a, b)

    def test_multi_args_with_lit(self):
        a = HTML("A&B", "&C", lit=True)
        b = "A&B&C"
        self.check(a, b)

    def test_one_arg_with_nl_and_lit(self):
        a = HTML("A&B", nl=True, lit=True)
        b = "A&B\n"
        self.check(a, b)

    def test_multi_args_with_nl_and_lit(self):
        a = HTML("A&B", "&C", nl=True, lit=True)
        b = "A&B\n&C\n"
        self.check(a, b)

    def test_raises_error_on_unknown_kwarg(self):
        with raises(TypeError):
            HTML("A", foo='bar')


class TestHTMLBuilder(HTMLTestCase):
    def test_html(self):
        a = HTML.a(href='http://mostlysafe\" <tag', c="Bad <script> tag")
        assert a == '<a href="http://mostlysafe&#34; &lt;tag">Bad &lt;script&gt; tag</a>'
        
        img = HTML.img(src="http://some/image.jpg")
        assert img == '<img src="http://some/image.jpg" />'
        
        br = HTML.br()
        assert "<br />" == br

    def test_unclosed_tag(self):
        result = HTML.form(_closed=False)
        assert "<form>" == result
        
        result = HTML.form(_closed=False, action="hello")
        assert '<form action="hello">' == result

    def test_newline_arg(self):
        assert HTML.a() ==         literal("<a></a>")
        assert HTML.a(_nl=True) == literal("<a>\n</a>\n")
        assert HTML.a(_closed=False) ==           literal("<a>")
        assert HTML.a(_closed=False, _nl=True) == literal("<a>\n")
        assert HTML.a("A", "B", href="/") ==      literal('<a href="/">AB</a>')
        assert HTML.a("A", "B", href="/", _nl=True) == literal('<a href="/">\nA\nB\n</a>\n')

    def test_tag_with_data_attr(self):
        assert HTML.span(data_foo="bar") == literal('<span data-foo="bar"></span>')

    def test_tag(self):
        a = HTML.tag("a", href="http://www.yahoo.com", name=None, 
            c="Click Here")
        b = literal('<a href="http://www.yahoo.com">Click Here</a>')
        self.check(a, b)
    
    def test_getattr(self):
        a =  HTML.a("Foo", href="http://example.com/", class_="important")
        b = literal('<a class="important" href="http://example.com/">Foo</a>')
        self.check(a, b)
    
    def test_cdata(self):
        a = HTML.cdata("Foo")
        b = literal("<![CDATA[Foo]]>")
        self.check(a, b)

    def test_cdata2(self):
        a = HTML.cdata(u"<p>")
        b = literal("<![CDATA[<p>]]>")
        self.check(a, b)

    def test_comment(self):
        a = HTML.comment("foo", "bar")
        b = "<!-- foobar -->"
        self.check(a, b)


class TestConstants(HTMLTestCase):
    def test_empty(self): self.check(HTML.EMPTY, "")
    def test_space(self): self.check(HTML.SPACE, " ")
    def test_br(self): self.check(HTML.BR, "<br />\n")
    def test_br2(self): self.check(HTML.BR2, "<br />\n<br />\n")
    def test_nl2(self): self.check(HTML.NL2, "\n\n")


class TestStyleAttribute(object):
    def test_list(self):
        a = {"style": ["margin:0", "padding: 0"]}
        b = {"style": "margin:0; padding: 0"}
        HTML.optimize_attrs(a)
        assert a == b

    def test_list2(self):
        a = {"style": ["margin:0", "padding: 0"], "href": ""}
        b = {"style": "margin:0; padding: 0", "href": ""}
        HTML.optimize_attrs(a)
        assert a == b

    def test_list_empty(self):
        a = {"style": []}
        b = {}
        HTML.optimize_attrs(a)
        assert a == b


class TestClassAttribute(object):    
    def test_list(self):
        a = {"class_": ["foo", "bar"]}
        b = {"class": "foo bar"}
        HTML.optimize_attrs(a)
        assert a == b

    def test_list2(self):
        a = {"class_": ["foo", "bar"], "class": "baz"}
        b = {"class": "foo bar"}
        HTML.optimize_attrs(a)
        assert a == b

    def test_list_empty(self):
        a = {"class": []}
        b = {}
        HTML.optimize_attrs(a)
        assert a == b
        
    def test_tuple(self):
        a = {"class": ("aa", "bb")}
        b = {"class": "aa bb"}
        HTML.optimize_attrs(a)
        assert a == b
    

    def test_conditional_list(self):
        a = {"class": [("first", False), ("even", True)] }
        b = {"class": "even"}
        HTML.optimize_attrs(a)
        assert a == b

    def test_conditional_list2(self):
        a = {"class": [("first", True), ("even", True)] }
        b = {"class": "first even"}
        HTML.optimize_attrs(a)
        assert a == b

    def test_conditional_list3(self):
        a = {"class": [("first", False), ("even", False)] }
        b = {}
        HTML.optimize_attrs(a)
        assert a == b


class TestAttributes(object):
    """Miscellaneous attribute tests."""

    def test_shouldnt_change_attrs(self):
        a = {"style": "aa", "class": "bb", "data-foo": "bar"}
        b = a
        HTML.optimize_attrs(a)
        assert a == b

    def test_multiple_optimizations(self):
        a = {"class_": ["A", "B"], "style": ["C", "D"], "bad": None}
        b = {"class": "A B", "style": "C; D", }
        HTML.optimize_attrs(a)
        assert a == b

    def test_delete_none(self):
        a = {"title": "Foo", "wicked": None}
        b = {"title": "Foo"}
        HTML.optimize_attrs(a)
        assert a == b

    def test_data(self):
        a = {"data_foo": "bar"}
        b = {"data-foo": "bar"}
        HTML.optimize_attrs(a)
        assert a == b

class TestBooleanAttributes(object):
    def test_boolean_true(self):
        a = {"defer": True, "disabled": "1", "multiple": 1, 
            "readonly": "readonly"}
        b = {"defer": "defer", "disabled": "disabled", "multiple": "multiple",
            "readonly": "readonly"}
        HTML.optimize_attrs(a)
        assert a == b

    def test_boolean_false(self):
        a = {"defer": False, "multiple": 0, "readonly": ""}
        b = {}
        HTML.optimize_attrs(a)
        assert a == b

    def test_boolean_true_with_additional_boolean_attr(self):
        a = {"defer": True, "data-foo": True}
        b = {"defer": "defer", "data-foo": "data-foo"}
        HTML.optimize_attrs(a, set(["data-foo"]))
        assert a == b

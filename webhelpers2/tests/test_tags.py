# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

import pytest
from pytest import raises
import six

from webhelpers2.html import HTML, literal
from webhelpers2.html.tags import *

from . import HTMLTestCase

#### Base classes ####

class OptionsTestCase(HTMLTestCase):
    def check_option(self, option, label, value):
        """Perform common tests on an ``Option``.

        I check the option's class, label, and value.
        """
        assert isinstance(option, Option)
        assert option.label == label
        assert option.value == value

    def check_options(self, options, count):
        """Perform common tests on an ``Options`` instance.

        I check the class and number of options, but not the options
        themselves.
        """
        assert isinstance(options, Options)
        assert len(options) == count

    def check_optgroup(self, optgroup, label, count):
        """Do common tests on an ``OptGroup``.

        I check the group's class, label, and number of options, but
        not the options themselves.
        """
        assert isinstance(optgroup, OptGroup)
        assert optgroup.label == label
        assert len(optgroup) == count


#### Test suites ####

class TestForm(HTMLTestCase):
    def test1(self):
        b = '<form action="http://www.example.com" method="post">'
        assert form(url="http://www.example.com") == b

    def test2(self):
        b = '<form action="http://www.example.com" method="GET">'
        assert form(url="http://www.example.com", method="GET") == b

    def test3(self):
        b = '<form action="/test/edit/1" method="post">'
        assert form("/test/edit/1") == b

    def test_form_multipart(self):
        b = '<form action="http://www.example.com" enctype="multipart/form-data" method="post">'
        assert form(url="http://www.example.com", multipart=True) == b
        
    def test4(self):
        a = form("/submit")
        b = literal('<form action="/submit" method="post">')
        self.check(a, b)

    def test4_get(self):
        a = form("/submit", method="get")
        b = literal('<form action="/submit" method="get">')
        self.check(a, b)

    def test4_put(self):
        a = form("/submit", method="put")
        b = literal('<form action="/submit" method="post"><div style="display:none">\n<input name="_method" type="hidden" value="put" />\n</div>\n')
        self.check(a, b)

    def test4_post(self):
        a = form("/submit", "post", multipart=True)
        b = literal('<form action="/submit" enctype="multipart/form-data" method="post">')
        self.check(a, b)

    def test_hidden_fields(self):
        tag = form("/submit", hidden_fields=[('foo', 'bar')])
        assert tag == literal( 
            '<form action="/submit" method="post">'
            '<div style="display:none">\n'
            '<input name="foo" type="hidden" value="bar" />\n'
            '</div>\n')

    def test_hidden_fields_from_dict(self):
        tag = form("/submit", hidden_fields={'foo': 'bar'})
        assert tag == literal(
            '<form action="/submit" method="post">'
            '<div style="display:none">\n'
            '<input name="foo" type="hidden" value="bar" />\n'
            '</div>\n')

    def test_end_form(self):
        a = end_form() 
        b = literal("</form>")
        self.check(a, b)


class TestInputHidden(HTMLTestCase):
    def test_hidden_field_int(self):
        b = '<input id="id" name="id" type="hidden" value="3" />'
        assert hidden("id", 3) == b

    def test_hidden_field(self):
        b = '<input id="id" name="id" type="hidden" value="3" />'
        assert hidden("id", "3") == b


class TestInputPassword(HTMLTestCase):
    def test_password_field(self):
        b = '<input id="password" name="password" type="password" />'
        assert password("password") == b


class TestInputCheckbox(HTMLTestCase):
    def test_check_box(self):
        a = checkbox("admin")
        b = '<input id="admin" name="admin" type="checkbox" value="1" />'
        self.check(a, b)

    def test_label_space(self):
        """Make sure there's a space between the widget and the label."""
        a = checkbox("admin", label="Check me")
        b = '<label><input id="admin" name="admin" type="checkbox" value="1" /> Check me</label>'
        self.check(a, b)

    def test_label_class(self):
        a = checkbox("admin", label="Check me", label_class="emphasize")
        b = '<label class="emphasize"><input id="admin" name="admin" type="checkbox" value="1" /> Check me</label>'
        self.check(a, b)


class TestInputRadio(HTMLTestCase):
    def test_radio_button(self):
        b = '<input id="people_justin" name="people" type="radio" value="justin" />'
        assert radio("people", "justin") == b

    def test2(self):
        b = '<input id="num_people_5" name="num_people" type="radio" value="5" />'
        assert radio("num_people", 5) == b

    def test3(self):
        b = '<input id="num_people_5" name="num_people" type="radio" value="5" />'
        assert radio("num_people", 5) == b
        
    def test4(self):
        b = '<input id="gender_m" name="gender" type="radio" value="m" /><input id="gender_f" name="gender" type="radio" value="f" />'
        assert radio("gender", "m") + radio("gender", "f") == b
        
    def test5(self):
        b = '<input id="opinion_-1" name="opinion" type="radio" value="-1" /><input id="opinion_1" name="opinion" type="radio" value="1" />'
        assert radio("opinion", "-1") + radio("opinion", "1") == b

    def test6(self):
        b = '<input checked="checked" id="num_people_5" name="num_people" type="radio" value="5" />'
        assert radio("num_people", 5, checked=True) == b

    def test_label_space(self):
        """Make sure there's a space between the widget and the label."""
        a = radio("gender", "m", label="Push me")
        b = '<label><input id="gender_m" name="gender" type="radio" value="m" /> Push me</label>'
        self.check(a, b)

    def test_label_class(self):
        """Make sure there's a space between the widget and the label."""
        a = radio("gender", "m", label="Push me", label_class="emphasize")
        b = '<label class="emphasize"><input id="gender_m" name="gender" type="radio" value="m" /> Push me</label>'
        self.check(a, b)


class TestInputSubmit(HTMLTestCase):
    def test_submit(self):
        b = '<input id="commit" name="commit" type="submit" value="Save changes" />'
        assert submit("commit", "Save changes") == b


class TestTextArea(HTMLTestCase):
    def test_text_area(self):
        b = '<textarea id="aa" name="aa"></textarea>'
        assert textarea("aa", "") == b

    def test2(self):
        b = '<textarea id="aa" name="aa"></textarea>'
        assert textarea("aa", None) == b
        
    def test3(self):
        b = '<textarea id="aa" name="aa">Hello!</textarea>'
        assert textarea("aa", "Hello!") == b

    def test_text_area_size_string(self):
        b = '<textarea cols="20" id="body" name="body" rows="40">hello world</textarea>'
        assert textarea("body", "hello world", cols=20, rows=40) == b

    def test4(self):
        a = textarea("body", "", cols=25, rows=10)
        b = literal('<textarea cols="25" id="body" name="body" rows="10"></textarea>')
        self.check(a, b)


class TestInputText(HTMLTestCase):
    def test_text_field(self):
        b = '<input id="title" name="title" type="text" value="" />'
        assert text("title", "") == b

    def test2(self):
        b = '<input id="title" name="title" type="text" />'
        assert text("title", None) == b


    def test3(self):
        b = '<input id="title" name="title" type="text" value="Hello!" />'
        assert text("title", "Hello!") == b

    def test_text_field_class_string(self):
        b = '<input class="admin" id="title" name="title" type="text" value="Hello!" />'
        assert text( "title", "Hello!", class_= "admin") == b


class TestInputOther(HTMLTestCase):
    def test_input_color(self):
        a = text("color", type="color")
        b = literal('<input id="color" name="color" type="color" />')
        self.check(a, b)

    def test_input_file(self):
        a = file("myfile")
        b = literal('<input id="myfile" name="myfile" type="file" />')
        self.check(a, b)


class TestBoolean(HTMLTestCase):
    def test_boolean_options(self):
        b = '<input checked="checked" disabled="disabled" id="admin" name="admin" readonly="readonly" type="checkbox" value="1" />'
        assert checkbox("admin", 1, True, disabled = True, readonly="yes") == b

    def test2(self):
        b = '<input checked="checked" id="admin" name="admin" type="checkbox" value="1" />'
        assert checkbox("admin", 1, True, disabled = False, readonly = None) == b


class TestAttributes(HTMLTestCase):
    # Don't set multiple id attributes for 'id_' argument.

    def test_multiple_id_bug(self):
        b = '<input id="eggs" name="spam" type="text" value="pizza" />'
        assert text("spam", "pizza", id="eggs") == b

    def test2(self):
        b = '<input id="eggs" name="spam" type="text" value="pizza" />'
        assert text("spam", "pizza", id_="eggs") == b

    def test3(self):
        b = '<select id="eggs" name="spam">\n<option selected="selected">2</option>\n</select>'
        assert select("spam", [1,2], [2], id="eggs") == b

    def test_id_and_id_(self):
        raises(TypeError, text, "spam", "pizza", id="fubar", id_="eggs")


class TestLinkHelper(HTMLTestCase):
    def test_link_tag_with_query(self):
        a = link_to("Hello", "http://www.example.com?q1=v1&q2=v2")
        b = "<a href=\"http://www.example.com?q1=v1&amp;q2=v2\">Hello</a>" 
        self.check(a, b)
    
    def test_link_tag_with_custom_onclick(self):
        a = link_to("Hello", "http://www.example.com", onclick="alert('yay!')")
        b = '<a href="http://www.example.com" onclick="alert(&#39;yay!&#39;)">Hello</a>'
        self.check(a, b)

    def test_link_to_default_label(self):
        self.check(
            link_to("", "http://www.example.com"),
            '<a href="http://www.example.com">http://www.example.com</a>')

    def test_link_to_if_true(self):
        a = link_to_if(True, "A", "B")
        b = '<a href="B">A</a>'
        self.check(a, b)

    def test_link_to_if_false(self):
        a = link_to_if(False, "A", "B")
        b = "A"
        self.check(a, b)

    def test_link_to_unless_true(self):
        a = link_to_unless(True, "A", "B")
        b = "A"
        self.check(a, b)

    def test_link_to_unless_false(self):
        a = link_to_unless(False, "A", "B")
        b = '<a href="B">A</a>'
        self.check(a, b)


class TestLinkClass(HTMLTestCase):
    def test_link_class(self):
        a = Link("Hello", "http://www.example.com/")
        b = '<a href="http://www.example.com/">Hello</a>'
        self.check(a.__html__(), b)

    def test_link_class_with_false_condition(self):
        a = Link("Hello", "http://www.example.com/")
        a.condition = False
        b = "Hello"
        self.check(a.__html__(), b)


class TestAssetTagHelper(HTMLTestCase):
    def test_auto_discovery_link_tag(self):
        a = auto_discovery_link('http://feed.com/feed.xml')
        b = literal('<link href="http://feed.com/feed.xml" rel="alternate" title="RSS" type="application/rss+xml" />')
        assert a == b

    def test2(self):
        a = auto_discovery_link("http://feed.com/feed.xml", feed_type="atom")
        b = '<link href="http://feed.com/feed.xml" rel="alternate" title="ATOM" type="application/atom+xml" />'
        assert a == b

    def test3(self):
        a = auto_discovery_link("app.rss", feed_type="atom", title="atom feed")
        b = '<link href="app.rss" rel="alternate" title="atom feed" type="application/atom+xml" />'
        assert a == b

    def test4(self):
        a = auto_discovery_link("app.rss", title="My RSS")
        b = '<link href="app.rss" rel="alternate" title="My RSS" type="application/rss+xml" />'
        assert a == b

    def test5(self):
        a = auto_discovery_link("/app.rss", feed_type="text/html")
        b = '<link href="/app.rss" rel="alternate" title="" type="text/html" />'
        assert a == b
        

class TestImage(HTMLTestCase):
    def test_image(self):
        a = image("/images/xml.png", "Xml")
        b = '<img alt="Xml" src="/images/xml.png" />'
        assert a == b

    def test2(self):
        a = image("/images/xml.png", alt="Xml")
        b = '<img alt="Xml" src="/images/xml.png" />'
        assert a == b

    def test3(self):
        a = image("/images/xml.png", "")
        b = '<img alt="" src="/images/xml.png" />'
        assert a == b

    def test4(self):
        a = image("/images/xml.png", None)
        b = '<img alt="" src="/images/xml.png" />'
        assert a == b

    def test5(self):
        a = image("/images/rss.png", "rss syndication")
        b = '<img alt="rss syndication" src="/images/rss.png" />'
        assert a == b

    def test6(self):
        a = image("gold.png", "Gold", height=70, width=45)
        b = '<img alt="Gold" height="70" src="gold.png" width="45" />'
        assert a == b

    def test7(self):
        a = image("/images/icon.png", height=10, width=16, alt="Edit Entry")
        b = '<img alt="Edit Entry" height="10" src="/images/icon.png" width="16" />'
        assert a == b

    def test8(self):
        a = image("/icons/icon.gif", "Icon", height=16, width=16)
        b = '<img alt="Icon" height="16" src="/icons/icon.gif" width="16" />'
        assert a == b

    def test9(self):
        a = image("/icons/icon.gif", "Icon", width=16)
        b = '<img alt="Icon" src="/icons/icon.gif" width="16" />'
        assert a == b

    def test_path_not_supported(self):
        with raises(TypeError) as exc_info:
            image("foo.png", 'foo', path="/tmp/foo.png")
        assert re.search(r"\bpath\b.*\bnot supported\b", str(exc_info.value))

    def test_use_pil_not_supported(self):
        with raises(TypeError) as exc_info:
            image("foo.png", 'foo', use_pil=True)
        assert re.search(r"\buse_pil\b.*\bnot supported\b",
                         str(exc_info.value))

class TestSelect(OptionsTestCase):
    def get_currency_options(self):
        opts = Options()
        opts.add_option("Dollar", "$")
        opts.add_option("Kroner", "DKK")
        return opts

    def test1(self):
        opts = self.get_currency_options()
        a = select("currency", "$", opts)
        b = literal('<select id="currency" name="currency">\n<option selected="selected" value="$">Dollar</option>\n<option value="DKK">Kroner</option>\n</select>')
        self.check(a, b)

    def test2(self):
        a = select("cc", "MasterCard", [ "VISA", "MasterCard" ], id="cc", class_="blue")
        b = literal('<select class="blue" id="cc" name="cc">\n<option>VISA</option>\n<option selected="selected">MasterCard</option>\n</select>')
        self.check(a, b)

    def test3(self):
        a = select("cc", ["VISA", "Discover"], [ "VISA", "MasterCard", "Discover" ])
        b = literal('<select id="cc" name="cc">\n<option selected="selected">VISA</option>\n<option>MasterCard</option>\n<option selected="selected">Discover</option>\n</select>')
        self.check(a, b)

    def test4(self):
        opts = self.get_currency_options()
        a = select("currency", None, opts, prompt="Please choose ...")
        b = literal('<select id="currency" name="currency">\n<option selected="selected" value="">Please choose ...</option>\n<option value="$">Dollar</option>\n<option value="DKK">Kroner</option>\n</select>')
        self.check(a, b)

    def test5(self):
        opts = [
            Option("Private", 1),
            Option("Semi-public", 2),
            Option("Public", 3),
            ]
        a = select("privacy", 3, opts)
        b = literal('<select id="privacy" name="privacy">\n<option value="1">Private</option>\n<option value="2">Semi-public</option>\n<option selected="selected" value="3">Public</option>\n</select>')
        self.check(a, b)

    def test6(self):
        opts = Options()
        users = opts.add_optgroup("Users")
        users.add_option("User1", "u1")
        users.add_option("User2", "u2")
        groups = opts.add_optgroup("Groups")
        groups.add_option("Group1", "g1")
        groups.add_option("Group2", "g2")
        a = select("recipients", None, opts)
        b = literal('<select id="recipients" name="recipients">\n<optgroup label="Users">\n<option value="u1">User1</option>\n<option value="u2">User2</option>\n</optgroup>\n<optgroup label="Groups">\n<option value="g1">Group1</option>\n<option value="g2">Group2</option>\n</optgroup>\n</select>')
        self.check(a, b)

    def test7(self):
        opts = [Option("No", False), Option("Yes", True)]
        a = select("enabled", True, opts)
        b = literal('<select id="enabled" name="enabled">\n<option value="False">No</option>\n<option selected="selected" value="True">Yes</option>\n</select>')
        self.check(a, b)


class TestOptGroup(OptionsTestCase):
    def test_repr(self):
        group = OptGroup("foo")
        group.add_option("baz", "bar")
        expected = "OptGroup(u'foo', [Option(u'baz', u'bar')])"
        if six.PY3:
            expected = expected.replace("u'", "'")
        assert repr(group) == expected


class TestOptionsArg(OptionsTestCase):
    def test1(self):
        with pytest.raises(TypeError):
            opts = Options(["A", 1, ("b", "B")])


class TestOptions(OptionsTestCase):
    def get_options(self):
        opts = Options()
        opts.add_option("A")
        opts.add_option(1)
        opts.add_option("B", "b")
        return opts

    def test1(self):
        a = self.get_options()
        self.check_options(a, 3)
        self.check_option(a[0], "A", None)
        self.check_option(a[1], 1, None)
        self.check_option(a[2], "B", "b")

    def test_html(self):
        opts = self.get_options()
        a = opts.render()
        b = literal('<option>A</option>\n<option>1</option>\n<option value="b">B</option>\n')
        self.check(a, b)

    def test_html_selected(self):
        selected_values = [1]
        opts = self.get_options()
        a = opts.render(selected_values)
        b = literal('<option>A</option>\n<option selected="selected">1</option>\n<option value="b">B</option>\n')
        self.check(a, b)

    def test_repr(self):
        opts = self.get_options()
        expected = "Options([Option(u'A', None), Option(1, None), Option(u'B', u'b')])"
        if six.PY3:
            expected = expected.replace("u'", "'")
        assert repr(opts) == expected


class TestThSortable(HTMLTestCase):
    def test1(self):
        sort = "name"
        a = th_sortable(sort, "name", "Name", "?sort=name")
        b = literal('<th class="sort">Name</th>')
        self.check(a, b)

    def test2(self):
        sort = "name"
        a = th_sortable(sort, "date", "Date", "?sort=date")
        b = literal('<th><a href="?sort=date">Date</a></th>')
        self.check(a, b)

    def test3(self):
        sort = "name"
        a = th_sortable(sort, "date", "Date", None, link_attrs={"onclick": "myfunc()"})
        b = literal('<th><a onclick="myfunc()">Date</a></th>')
        self.check(a, b)


class TestUl(HTMLTestCase):
    def test1(self):
        a = ul(["foo", "bar"])
        b = literal('<ul>\n<li>foo</li>\n<li>bar</li>\n</ul>')
        self.check(a, b)

    def test2(self):
        a = ul(["A", "B"], li_attrs={"class_": "myli"}, class_="mylist") 
        b = literal('<ul class="mylist">\n<li class="myli">A</li>\n<li class="myli">B</li>\n</ul>')
        self.check(a, b)

    def test3(self):
        a = ul([]) 
        b = '<ul></ul>'
        self.check(a, b)

    def test4(self):
        a = ul([], default=literal(""))
        b = ""
        self.check(a, b)

    def test5(self):
        a = ul([], default=literal('<span class="no-data">No data</span>'))
        b = literal('<span class="no-data">No data</span>')
        self.check(a, b)

    def test6(self):
        a = ul(["A"], default="NOTHING")
        b = literal('<ul>\n<li>A</li>\n</ul>')
        self.check(a, b)


class TestOl(HTMLTestCase):
    def test(self):
        a = ol(["foo", "bar"])
        b = literal('<ol>\n<li>foo</li>\n<li>bar</li>\n</ol>')
        self.check(a, b)

    def test2(self):
        a = ol(["A", "B"], li_attrs={"class_": "myli"}, class_="mylist") 
        b = literal('<ol class="mylist">\n<li class="myli">A</li>\n<li class="myli">B</li>\n</ol>')
        self.check(a, b)

    def test3(self):
        a = ol([])
        b = ""
        self.check(a, b)


class TestJavascriptLink(HTMLTestCase):
    def test_javascript_include_tag(self):
        a = javascript_link('/javascripts/prototype.js', '/other-javascripts/util.js')
        b = '<script src="/javascripts/prototype.js" type="text/javascript"></script>\n<script src="/other-javascripts/util.js" type="text/javascript"></script>'
        self.check(a, b)

    def test_with_defer(self):
        a = javascript_link("/js/pngfix.js", defer=True)
        b = """<script defer="defer" src="/js/pngfix.js" type="text/javascript"></script>"""
        self.check(a, b)

class TestStylesheetLink(HTMLTestCase):
    def test_stylesheet_link_tag(self):
        a = stylesheet_link("/dir/file.css", media="all")
        b = literal('<link href="/dir/file.css" media="all" rel="stylesheet" type="text/css" />')
        self.check(a, b)
    def test2(self):
        a = stylesheet_link("style.css", media="all")
        b = '<link href="style.css" media="all" rel="stylesheet" type="text/css" />'
        self.check(a, b)

    def test3(self):
        a = stylesheet_link("/random.styles", "/css/stylish.css")
        b = '<link href="/random.styles" media="screen" rel="stylesheet" type="text/css" />\n<link href="/css/stylish.css" media="screen" rel="stylesheet" type="text/css" />'
        self.check(a, b)


    def test4(self):
        a = stylesheet_link('/stylesheets/style.css')
        b = literal('<link href="/stylesheets/style.css" media="screen" rel="stylesheet" type="text/css" />')
        self.check(a, b)

    def test5(self):
        a = stylesheet_link('/stylesheets/dir/file.css', media='all')
        b = literal('<link href="/stylesheets/dir/file.css" media="all" rel="stylesheet" type="text/css" />')
        self.check(a, b)

    def test_href_not_supported(self):
        with raises(TypeError) as exc_info:
            stylesheet_link('/file.css', href="foo.css")
        assert re.search(r'\bhref\b.* not allowed\b', str(exc_info.value))

class TestAutoDiscoveryLink(HTMLTestCase):
    def test1(self):
        a = auto_discovery_link('http://feed.com/feed.xml')
        b = literal('<link href="http://feed.com/feed.xml" rel="alternate" title="RSS" type="application/rss+xml" />')
        self.check(a, b)

    def test2(self):
        a = auto_discovery_link('http://feed.com/feed.xml', feed_type='atom')
        b = literal('<link href="http://feed.com/feed.xml" rel="alternate" title="ATOM" type="application/atom+xml" />')
        self.check(a, b)

    def test3(self):
        a = auto_discovery_link('app.rss', feed_type='atom', title='atom feed')
        b = literal('<link href="app.rss" rel="alternate" title="atom feed" type="application/atom+xml" />')
        self.check(a, b)

    def test4(self):
        a = auto_discovery_link('/app.html', feed_type='text/html')
        b = literal('<link href="/app.html" rel="alternate" title="" type="text/html" />')
        self.check(a, b)

    def test_href_not_supported(self):
        with raises(TypeError) as exc_info:
            auto_discovery_link('/app.html', href="foo.html")
        assert re.search(r'\bhref\b.* not allowed\b', str(exc_info.value))

    def test_type_not_supported(self):
        with raises(TypeError) as exc_info:
            auto_discovery_link('/app.html', type="text/html")
        assert re.search(r'\btype\b.* not allowed\b', str(exc_info.value))

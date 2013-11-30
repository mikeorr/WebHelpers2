# -*- coding: utf-8 -*-
"""Tests ported from former html.tags doctests.
"""
from __future__ import unicode_literals

import pytest
from pytest import raises

from webhelpers2.html import HTML, literal
from webhelpers2.html.tags import *


class TestForm(object):
    def test4(self):
        b = literal('<form action="/submit" method="post">')
        assert form("/submit") == b

    def test4_get(self):
        b = literal('<form action="/submit" method="get">')
        assert form("/submit", method="get") == b

    def test4_put(self):
        b = literal('<form action="/submit" method="post"><div style="display:none">\n<input name="_method" type="hidden" value="put" />\n</div>\n')
        assert form("/submit", method="put") == b

    def test4_post(self):

        b = literal('<form action="/submit" enctype="multipart/form-data" method="post">')
        assert form("/submit", "post", multipart=True) == b

    def test_end_form(self):
        assert end_form() == literal("</form>")


class TestInputCheckbox(object):
    def test_check_box(self):
        b = '<input id="admin" name="admin" type="checkbox" value="1" />'
        assert checkbox("admin") == b


class TestTextArea(object):
    def test4(self):
        b = literal('<textarea cols="25" id="body" name="body" rows="10"></textarea>')
        assert textarea("body", "", cols=25, rows=10) == b


class TestInputOther(object):
    def test_input_color(self):
        b = literal('<input id="color" name="color" type="color" />')
        assert text("color", type="color") == b

    def test_input_file(self):
        b = literal('<input id="myfile" name="myfile" type="file" />')
        assert file("myfile") == b


@pytest.mark.xfail(reason="Selected options not being set properly.")
class TestSelect(object):
    def test1(self):
        a = select("currency", "$", [["$", "Dollar"], ["DKK", "Kroner"]])
        b = literal('<select id="currency" name="currency">\n<option selected="selected" value="$">Dollar</option>\n<option value="DKK">Kroner</option>\n</select>')
        assert a == b

    def test2(self):
        a = select("cc", "MasterCard", [ "VISA", "MasterCard" ], id="cc", class_="blue")
        b = literal('<select class="blue" id="cc" name="cc">\n<option value="VISA">VISA</option>\n<option selected="selected" value="MasterCard">MasterCard</option>\n</select>')
        assert a == b

    def test3(self):
        a = select("cc", ["VISA", "Discover"], [ "VISA", "MasterCard", "Discover" ])
        b = literal('<select id="cc" name="cc">\n<option selected="selected" value="VISA">VISA</option>\n<option value="MasterCard">MasterCard</option>\n<option selected="selected" value="Discover">Discover</option>\n</select>')
        assert a == b

    def test4(self):
        a = select("currency", None, [["$", "Dollar"], ["DKK", "Kroner"]], prompt="Please choose ...")
        b = literal('<select id="currency" name="currency">\n<option selected="selected" value="">Please choose ...</option>\n<option value="$">Dollar</option>\n<option value="DKK">Kroner</option>\n</select>')

    def test5(self):
        a = select("privacy", 3, [(1, "Private"), (2, "Semi-public"), (3, "Public")])
        b = literal('<select id="privacy" name="privacy">\n<option value="1">Private</option>\n<option value="2">Semi-public</option>\n<option selected="selected" value="3">Public</option>\n</select>')
        assert a == b

    def test6(self):
        a = select("recipients", None, [([("u1", "User1"), ("u2", "User2")], "Users"), ([("g1", "Group1"), ("g2", "Group2")], "Groups")])
        b = literal('<select id="recipients" name="recipients">\n<optgroup label="Users">\n<option value="u1">User1</option>\n<option value="u2">User2</option>\n</optgroup>\n<optgroup label="Groups">\n<option value="g1">Group1</option>\n<option value="g2">Group2</option>\n</optgroup>\n</select>')
        assert a == b


class TestOptions(object):
    def get_options(self):
        return Options(["A", 1, ("b", "B")])

    def test1(self):
        opts = self.get_options()
        assert opts == Options([("A", "A"), ("1", "1"), ("b", "B")])

    def test_list_values(self):
        opts = self.get_options()
        assert list(opts.values()) == ["A", "1", "b"]

    def test_opts_2_value(self):
        opts = self.get_options()
        assert opts[2].value == "b"

    def test_opts_2_label(self):
        opts = self.get_options()
        assert opts[2].label == "B"


class TestTitle(object):
    def test1(self):
        b = literal('<span class="not-required">First Name</span>')
        assert title("First Name") == b

    def test2(self):
        b = literal('<span class="required">Last Name <span class="required-symbol">*</span></span>')
        assert title("Last Name", True) == b

    def test3(self):
        b = literal(u'<span class="not-required"><label for="fname">First Name</label></span>')
        assert title("First Name", False, "fname") == b

    def test4(self):
        b = literal('<span class="required"><label for="lname">Last Name</label> <span class="required-symbol">*</span></span>')
        assert title("Last Name", True, label_for="lname") == b


class TestThSortable(object):
    def test1(self):
        sort = "name"
        b = literal('<th class="sort">Name</th>')
        assert th_sortable(sort, "name", "Name", "?sort=name") == b

    def test2(self):
        sort = "name"
        b = literal('<th><a href="?sort=date">Date</a></th>')
        assert th_sortable(sort, "date", "Date", "?sort=date") == b

    def test3(self):
        sort = "name"
        a = th_sortable(sort, "date", "Date", None, link_attrs={"onclick": "myfunc()"})
        b = literal('<th><a onclick="myfunc()">Date</a></th>')
        assert a == b


class TestUl(object):
    def test1(self):
        b = literal('<ul>\n<li>foo</li>\n<li>bar</li>\n</ul>')
        assert ul(["foo", "bar"]) == b

    def test2(self):
        a = ul(["A", "B"], li_attrs={"class_": "myli"}, class_="mylist") 
        b = literal('<ul class="mylist">\n<li class="myli">A</li>\n<li class="myli">B</li>\n</ul>')
        assert a == b

    def test3(self):
        assert ul([]) == literal('<ul></ul>')

    def test4(self):
        assert ul([], default="") == ''

    def test5(self):
        a = ul([], default=literal('<span class="no-data">No data</span>'))
        b = literal('<span class="no-data">No data</span>')
        assert a == b

    def test6(self):
        a = ul(["A"], default="NOTHING")
        b = literal('<ul>\n<li>A</li>\n</ul>')
        assert a == b


class TestOl(object):
    def test(self):
        b = literal('<ol>\n<li>foo</li>\n<li>bar</li>\n</ol>')
        assert ol(["foo", "bar"]) == b

    def test2(self):
        a = ol(["A", "B"], li_attrs={"class_": "myli"}, class_="mylist") 
        b = literal('<ol class="mylist">\n<li class="myli">A</li>\n<li class="myli">B</li>\n</ol>')
        assert a == b

    def test3(self):
        assert ol([]) == literal('')


class TestImage(object):
    def test1(self):
        a = image('/images/rss.png', 'rss syndication')
        b = literal('<img alt="rss syndication" src="/images/rss.png" />')
        assert a == b

    def test2(self):
        a = image('/images/xml.png', "")
        b = literal('<img alt="" src="/images/xml.png" />')
        assert a == b

    def test3(self):
        a = image("/images/icon.png", height=16, width=10, alt="Edit Entry")
        b = literal('<img alt="Edit Entry" height="16" src="/images/icon.png" width="10" />')
        assert a == b

    def test4(self):
        a = image("/icons/icon.gif", alt="Icon", width=16, height=16)
        b = literal('<img alt="Icon" height="16" src="/icons/icon.gif" width="16" />')
        assert a == b

    def test5(self):
        a = image("/icons/icon.gif", None, width=16)
        b = literal('<img alt="" src="/icons/icon.gif" width="16" />')
        assert a == b

 
class TestCSSClasses(object):
    def test1(self):
        arg = [("first", False), ("even", True)]
        b = literal('<td class="even">My content.</td>')
        assert HTML.td("My content.", class_=css_classes(arg)) == b

    def test2(self):
        arg = [("first", True), ("even", True)]
        b = literal('<td class="first even">My content.</td>')
        assert HTML.td("My content.", class_=css_classes(arg)) == b

    def test3(self):
        a = arg = [("first", False), ("even", False)]
        b = HTML.td("My content.", class_=css_classes(arg))
        assert literal(u'<td>My content.</td>') == b


class TestJavascriptLink(object):
    def test1(self):
        a = javascript_link('/javascripts/prototype.js', '/other-javascripts/util.js')
        b = '<script src="/javascripts/prototype.js" type="text/javascript"></script>\n<script src="/other-javascripts/util.js" type="text/javascript"></script>'
        assert a == b

    def test2(self):
        a = javascript_link('/app.js', '/test/test.1.js')
        b = '<script src="/app.js" type="text/javascript"></script>\n<script src="/test/test.1.js" type="text/javascript"></script>'
        assert a == b


class StylesheetLink(object):
    def test1(self):
        b = literal('<link href="/stylesheets/style.css" media="screen" rel="stylesheet" type="text/css" />')
        assert stylesheet_link('/stylesheets/style.css') == b

    def test2(self):
        b = literal('<link href="/stylesheets/dir/file.css" media="all" rel="stylesheet" type="text/css" />')
        assert stylesheet_link('/stylesheets/dir/file.css', media='all') == b

        
class TestAutoDiscoveryLink(object):
    def test1(self):
        b = literal('<link href="http://feed.com/feed.xml" rel="alternate" title="RSS" type="application/rss+xml" />')
        assert auto_discovery_link('http://feed.com/feed.xml') == b

    def test2(self):
        a = auto_discovery_link('http://feed.com/feed.xml', feed_type='atom')
        b = literal('<link href="http://feed.com/feed.xml" rel="alternate" title="ATOM" type="application/atom+xml" />')
        assert a == b

    def test3(self):
        a = auto_discovery_link('app.rss', feed_type='atom', title='atom feed')
        b = literal('<link href="app.rss" rel="alternate" title="atom feed" type="application/atom+xml" />')
        assert a == b

    def test4(self):
        a = auto_discovery_link('/app.html', feed_type='text/html')
        b = literal('<link href="/app.html" rel="alternate" title="" type="text/html" />')
        assert a == b

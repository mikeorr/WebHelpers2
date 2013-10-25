# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pytest import raises

from webhelpers2.html import HTML, literal
from webhelpers2.html.tags import *

class TestFormTagHelper(object):
    def test_check_box(self):
        b = '<input id="admin" name="admin" type="checkbox" value="1" />'
        assert checkbox("admin") == b

    def test_form(self):
        b = '<form action="http://www.example.com" method="post">'
        assert form(url="http://www.example.com") == b

        b = '<form action="http://www.example.com" method="GET">'
        assert form(url="http://www.example.com", method="GET") == b

        b = '<form action="/test/edit/1" method="post">'
        assert form("/test/edit/1") == b

    def test_form_multipart(self):
        b = '<form action="http://www.example.com" enctype="multipart/form-data" method="post">'
        assert form(url="http://www.example.com", multipart=True) == b
        
    def test_hidden_field(self):
        b = '<input id="id" name="id" type="hidden" value="3" />'
        assert hidden("id", 3) == b

    def test_hidden_field_alt(self):
        b = '<input id="id" name="id" type="hidden" value="3" />'
        assert hidden("id", "3") == b

    def test_password_field(self):
        b = '<input id="password" name="password" type="password" />'
        assert password("password") == b

    def test_radio_button(self):
        b = '<input id="people_justin" name="people" type="radio" value="justin" />'
        assert radio("people", "justin") == b

        b = '<input id="num_people_5" name="num_people" type="radio" value="5" />'
        assert radio("num_people", 5) == b

        b = '<input id="num_people_5" name="num_people" type="radio" value="5" />'
        assert radio("num_people", 5) == b
        
        b = '<input id="gender_m" name="gender" type="radio" value="m" /><input id="gender_f" name="gender" type="radio" value="f" />'
        assert radio("gender", "m") + radio("gender", "f") == b
        
        b = '<input id="opinion_-1" name="opinion" type="radio" value="-1" /><input id="opinion_1" name="opinion" type="radio" value="1" />'
        assert radio("opinion", "-1") + radio("opinion", "1") == b

        b = '<input checked="checked" id="num_people_5" name="num_people" type="radio" value="5" />'
        assert radio("num_people", 5, checked=True) == b

    def test_submit(self):
        b = '<input id="commit" name="commit" type="submit" value="Save changes" />'
        assert submit("commit", "Save changes") == b

    def test_text_area(self):
        b = '<textarea id="aa" name="aa"></textarea>'
        assert textarea("aa", "") == b

        b = '<textarea id="aa" name="aa"></textarea>'
        assert textarea("aa", None) == b
        
        b = '<textarea id="aa" name="aa">Hello!</textarea>'
        assert textarea("aa", "Hello!") == b

    def test_text_area_size_string(self):
        b = '<textarea cols="20" id="body" name="body" rows="40">hello world</textarea>'
        assert textarea("body", "hello world", cols=20, rows=40) == b

    def test_text_field(self):
        b = '<input id="title" name="title" type="text" value="" />'
        assert text("title", "") == b

        b = '<input id="title" name="title" type="text" />'
        assert text("title", None) == b

        b = '<input id="title" name="title" type="text" value="Hello!" />'
        assert text("title", "Hello!") == b

    def test_text_field_class_string(self):
        b = '<input class="admin" id="title" name="title" type="text" value="Hello!" />'
        assert text( "title", "Hello!", class_= "admin") == b

    def test_boolean_options(self):
        b = '<input checked="checked" disabled="disabled" id="admin" name="admin" readonly="readonly" type="checkbox" value="1" />'
        assert checkbox("admin", 1, True, disabled = True, readonly="yes") == b

        b = '<input checked="checked" id="admin" name="admin" type="checkbox" value="1" />'
        assert checkbox("admin", 1, True, disabled = False, readonly = None) == b

    def test_multiple_id_bug(self):
        # Don't set multiple id attributes for 'id_' argument.
        b = '<input id="eggs" name="spam" type="text" value="pizza" />'
        assert text("spam", "pizza", id="eggs") == b

        b = '<input id="eggs" name="spam" type="text" value="pizza" />'
        assert text("spam", "pizza", id_="eggs") == b

        b = '<select id="eggs" name="spam">\n<option selected="selected" value="2">2</option>\n</select>'
        assert select("spam", [1,2], [2], id="eggs") == b

        b = '<select id="eggs" name="spam">\n<option selected="selected" value="2">2</option>\n</select>'
        assert select("spam", [1,2], [2], id_="eggs") == b

    def test_id_and_id_(self):
        raises(TypeError, text, "spam", "pizza", id="fubar", id_="eggs")
        

    
class TestLinkHelper(object):
    def test_link_tag_with_query(self):
        b = "<a href=\"http://www.example.com?q1=v1&amp;q2=v2\">Hello</a>" 
        assert link_to("Hello", "http://www.example.com?q1=v1&q2=v2") == b
    
    def test_link_tag_with_query_and_no_name(self):
        a = link_to(None, HTML.literal("http://www.example.com?q1=v1&amp;q2=v2"))
        b = "<a href=\"http://www.example.com?q1=v1&amp;q2=v2\">http://www.example.com?q1=v1&amp;q2=v2</a>" 
        assert a == b
    
    def test_link_tag_with_custom_onclick(self):
        a = link_to("Hello", "http://www.example.com", onclick="alert('yay!')")
        b = '<a href="http://www.example.com" onclick="alert(&#39;yay!&#39;)">Hello</a>'
        assert a == b
    

class TestAssetTagHelper(object):
    def test_auto_discovery_link_tag(self):
        a = auto_discovery_link('http://feed.com/feed.xml')
        b = literal('<link href="http://feed.com/feed.xml" rel="alternate" title="RSS" type="application/rss+xml" />')
        assert a == b

        a = auto_discovery_link("http://feed.com/feed.xml", feed_type="atom")
        b = '<link href="http://feed.com/feed.xml" rel="alternate" title="ATOM" type="application/atom+xml" />'
        assert a == b

        a = auto_discovery_link("app.rss", feed_type="atom", title="atom feed")
        b = '<link href="app.rss" rel="alternate" title="atom feed" type="application/atom+xml" />'
        assert a == b

        a = auto_discovery_link("app.rss", title="My RSS")
        b = '<link href="app.rss" rel="alternate" title="My RSS" type="application/rss+xml" />'
        assert a == b

        a = auto_discovery_link("/app.rss", feed_type="text/html")
        b = '<link href="/app.rss" rel="alternate" title="" type="text/html" />'
        assert a == b

        a = auto_discovery_link("/app.html", title="My RSS", feed_type="text/html")
        b = '<link href="/app.html" rel="alternate" title="My RSS" type="text/html" />'
        assert a == b
        
    def test_image(self):
        a = image("/images/xml.png", "Xml")
        b = '<img alt="Xml" src="/images/xml.png" />'
        assert a == b

        a = image("/images/xml.png", alt="Xml")
        b = '<img alt="Xml" src="/images/xml.png" />'
        assert a == b

        a = image("/images/xml.png", "")
        b = '<img alt="" src="/images/xml.png" />'
        assert a == b

        a = image("/images/xml.png", None)
        b = '<img alt="" src="/images/xml.png" />'
        assert a == b

        a = image("/images/rss.png", "rss syndication")
        b = '<img alt="rss syndication" src="/images/rss.png" />'
        assert a == b

        a = image("gold.png", "Gold", height=70, width=45)
        b = '<img alt="Gold" height="70" src="gold.png" width="45" />'
        assert a == b

        a = image("/images/icon.png", height=10, width=16, alt="Edit Entry")
        b = '<img alt="Edit Entry" height="10" src="/images/icon.png" width="16" />'
        assert a == b

        a = image("/icons/icon.gif", "Icon", height=16, width=16)
        b = '<img alt="Icon" height="16" src="/icons/icon.gif" width="16" />'
        assert a == b

        a = image("/icons/icon.gif", "Icon", width=16)
        b = '<img alt="Icon" src="/icons/icon.gif" width="16" />'
        assert a == b

    def test_javascript_include_tag(self):
        a = javascript_link("/javascripts/prototype.js", "/other-javascripts/util.js")
        b = """<script src="/javascripts/prototype.js" type="text/javascript"></script>\n<script src="/other-javascripts/util.js" type="text/javascript"></script>"""
        assert a == b

        a = javascript_link("/js/pngfix.js", defer=True)
        b = """<script defer="defer" src="/js/pngfix.js" type="text/javascript"></script>"""
        assert a == b

    def test_stylesheet_link_tag(self):
        a = stylesheet_link("/dir/file.css", media="all")
        b = literal('<link href="/dir/file.css" media="all" rel="stylesheet" type="text/css" />')
        assert a == b

        a = stylesheet_link("style.css", media="all")
        b = '<link href="style.css" media="all" rel="stylesheet" type="text/css" />'
        assert a == b

        a = stylesheet_link("/random.styles", "/css/stylish.css")
        b = '<link href="/random.styles" media="screen" rel="stylesheet" type="text/css" />\n<link href="/css/stylish.css" media="screen" rel="stylesheet" type="text/css" />'
        assert a == b

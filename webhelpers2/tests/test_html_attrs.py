from __future__ import unicode_literals

from nose.tools import eq_

from webhelpers2.html import literal, escape, HTML
from webhelpers2.html.builder import _attr_decode
from webhelpers2.html.builder import format_attrs

def test_style_arg1():
    style = ["margin:0", "padding: 0"]
    control = literal(' style="margin:0; padding: 0"')
    eq_(format_attrs(style=style), control)

def test_style_arg2():
    style = ["margin:0", "padding: 0"]
    control = literal(' maxwidth="10" style="margin:0; padding: 0"')
    eq_(format_attrs(style=style, maxwidth=10), control)
    
def test_class_arg1():
    class_ = ["foo", "bar"]
    control = literal(' class="foo bar"')
    eq_(format_attrs(class_=class_), control)

def test_class_arg2():
    class_ = ["foo", "bar"]
    args = {"class_": class_, "class": "baz"}
    control = literal(' class="foo bar"')
    eq_(format_attrs(**args), control)
    

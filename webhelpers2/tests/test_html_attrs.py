from __future__ import unicode_literals

from webhelpers2.html import literal, escape, HTML
from webhelpers2.html.builder import _attr_decode
from webhelpers2.html.builder import format_attrs

def test_style_arg1():
    a = {"style": ["margin:0", "padding: 0"]}
    b = {"style": "margin:0; padding: 0"}
    HTML.optimize_attrs(a)
    assert a == b

def test_style_arg2():
    a = {"style": ["margin:0", "padding: 0"], "maxwidth": 10}
    b = {"style": "margin:0; padding: 0", "maxwidth": 10}
    HTML.optimize_attrs(a)
    assert a == b
    
def test_class_arg1():
    a = {"class_": ["foo", "bar"]}
    b = {"class": "foo bar"}
    HTML.optimize_attrs(a)
    assert a == b

def test_class_arg2():
    a = {"class_": ["foo", "bar"], "class": "baz"}
    b = {"class": "foo bar"}
    HTML.optimize_attrs(a)
    assert a == b
    

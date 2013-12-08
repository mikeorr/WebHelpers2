from __future__ import unicode_literals

from webhelpers2.html import literal, escape, HTML

def test_style_attr_list():
    a = {"style": ["margin:0", "padding: 0"]}
    b = {"style": "margin:0; padding: 0"}
    HTML.optimize_attrs(a)
    assert a == b

def test_style_attr_list2():
    a = {"style": ["margin:0", "padding: 0"], "href": ""}
    b = {"style": "margin:0; padding: 0", "href": ""}
    HTML.optimize_attrs(a)
    assert a == b

def test_style_attr_list_empty():
    a = {"style": []}
    b = {}
    HTML.optimize_attrs(a)
    assert a == b
    
def test_class_attr_list():
    a = {"class_": ["foo", "bar"]}
    b = {"class": "foo bar"}
    HTML.optimize_attrs(a)
    assert a == b

def test_class_attr_list2():
    a = {"class_": ["foo", "bar"], "class": "baz"}
    b = {"class": "foo bar"}
    HTML.optimize_attrs(a)
    assert a == b

def test_class_attr_list_empty():
    a = {"class": []}
    b = {}
    HTML.optimize_attrs(a)
    assert a == b
    
def test_class_attr_tuple():
    a = {"class": ("aa", "bb")}
    b = {"class": "aa bb"}
    HTML.optimize_attrs(a)
    assert a == b
    
def test_data_attr():
    a = {"data_foo": "bar"}
    b = {"data-foo": "bar"}
    HTML.optimize_attrs(a)
    assert a == b

def test_shouldnt_change_attrs():
    a = {"style": "aa", "class": "bb", "data-foo": "bar"}
    b = a
    HTML.optimize_attrs(a)
    assert a == b

def test_multiple_optimizations():
    a = {"class_": ["A", "B"], "style": ["C", "D"], "bad": None}
    b = {"class": "A B", "style": "C; D", }
    HTML.optimize_attrs(a)
    assert a == b

def test_delete_none():
    a = {"title": "Foo", "wicked": None}
    b = {"title": "Foo"}
    HTML.optimize_attrs(a)
    assert a == b

def test_boolean_true():
    a = {"defer": True, "disabled": "1", "multiple": 1, "readonly": "readonly"}
    b = {"defer": "defer", "disabled": "disabled", "multiple": "multiple",
        "readonly": "readonly"}
    HTML.optimize_attrs(a)
    assert a == b

def test_boolean_false():
    a = {"defer": False, "multiple": 0, "readonly": ""}
    b = {}
    HTML.optimize_attrs(a)
    assert a == b

def test_boolean_true_with_additional_boolean_attr():
    a = {"defer": True, "data-foo": True}
    b = {"defer": "defer", "data-foo": "data-foo"}
    HTML.optimize_attrs(a, {"data-foo"})
    assert a == b

from webhelpers2.html import HTML
from webhelpers2.html.tags import *

class Holder(object):
    def __init__(self, settings):
        for k,v in settings.items():
            setattr(self, k, v)
            
class TestModelTagsHelperWithObject(object):
    def setup_method(self, method):
        obj = Holder({"name":"Jim", "phone":"123-456-7890", "fulltime":True, "fired":False, "password":"bacon", "longtext":"lorem ipsum lorem ipsum\n"*10, "favcolor":"blue", "lang":"en"})
        self.m = ModelTags(obj)
        
    def test_check_box(self):
        b = '<input checked="checked" id="fulltime" name="fulltime" type="checkbox" value="1" />'
        assert self.m.checkbox("fulltime") == b

    def test_hidden_field(self):
        b = '<input id="name" name="name" type="hidden" value="Jim" />'
        assert self.m.hidden("name") == b

    def test_password_field(self):
        b = '<input id="name" name="name" type="password" value="Jim" />'
        assert self.m.password("name") == b

    def test_file_field(self):
       b = '<input id="name" name="name" type="file" value="Jim" />'
       assert self.m.file("name") == b

    def test_radio_button(self):
       b = '<input checked="checked" id="favcolor_blue" name="favcolor" type="radio" value="blue" />'
       assert self.m.radio("favcolor", "blue") == b
        
    def test_radio_button2(self):
       b = '<input id="favcolor_red" name="favcolor" type="radio" value="red" />'
       assert self.m.radio("favcolor", "red") == b

    def test_text_area(self):
       b = '<textarea id="longtext" name="longtext">lorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\n</textarea>'
       assert self.m.textarea("longtext") == b

    def test_text_field(self):
       b = '<input id="name" name="name" type="text" value="Jim" />'
       assert self.m.text("name") == b

    def test_select(self):
       a = self.m.select("lang", [("en", "English"), ("de", "German"), ("jp", "Japanese")])
       b = '<select id="lang" name="lang">\n<option selected="selected" value="en">English</option>\n<option value="de">German</option>\n<option value="jp">Japanese</option>\n</select>'
       assert a == b


class TestModelTagsHelperWithDict(TestModelTagsHelperWithObject):
    def setup_method(self, method):
        obj = {"name":"Jim", "phone":"123-456-7890", "fulltime":True, "fired":False, "password":"bacon", "longtext":"lorem ipsum lorem ipsum\n"*10, "favcolor":"blue", "lang":"en"}
        self.m = ModelTags(obj, use_keys=True)

    def test_check_box(self):
        b = '<input checked="checked" id="fulltime" name="fulltime" type="checkbox" value="1" />'
        assert self.m.checkbox("fulltime") == b

    def test_hidden_field(self):
        b = '<input id="name" name="name" type="hidden" value="Jim" />'
        assert self.m.hidden("name") == b

    def test_password_field(self):
        b = '<input id="name" name="name" type="password" value="Jim" />'
        assert self.m.password("name") == b

    def test_file_field(self):
        b = '<input id="name" name="name" type="file" value="Jim" />'
        assert self.m.file("name") == b

    def test_radio_button(self):
        b = '<input checked="checked" id="favcolor_blue" name="favcolor" type="radio" value="blue" />'
        assert self.m.radio("favcolor", "blue") == b

    def test_radio_button2(self):
        b = '<input id="favcolor_red" name="favcolor" type="radio" value="red" />'
        assert self.m.radio("favcolor", "red") == b

    def test_text_area(self):
        b = '<textarea id="longtext" name="longtext">lorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\n</textarea>'
        assert self.m.textarea("longtext") == b

    def test_text_field(self):
        b = '<input id="name" name="name" type="text" value="Jim" />'
        assert self.m.text("name") == b

    def test_select(self):
        a = self.m.select("lang", [("en", "English"), ("de", "German"), ("jp", "Japanese")])
        b = '<select id="lang" name="lang">\n<option selected="selected" value="en">English</option>\n<option value="de">German</option>\n<option value="jp">Japanese</option>\n</select>'
        assert a == b


class TestIdGeneration(object):
    def check_id_format_syntax(self, id_format):
        m = ModelTags(None, id_format=id_format)
        a = {}
        b = {"id": "person:foo"}
        m._update_id("foo", a)
        assert a == b

    def test_braces_syntax(self):
        self.check_id_format_syntax("person:{}")

    def test_percent_syntax(self):
        """Backward compatibility with WebHelpers."""
        self.check_id_format_syntax("person:%s")


class TestModelTagsHelperWithIdGeneration(TestModelTagsHelperWithObject):
    def setup_method(self, method):
        obj = Holder({"name":"Jim", "phone":"123-456-7890", "fulltime":True, "fired":False, "password":"bacon", "longtext":"lorem ipsum lorem ipsum\n"*10, "favcolor":"blue", "lang":"en"})
        self.m = ModelTags(obj, id_format="person:%s")

    def test_check_box(self):
        b = '<input checked="checked" id="person:fulltime" name="fulltime" type="checkbox" value="1" />'
        assert self.m.checkbox("fulltime") == b

    def test_hidden_field(self):
        b = '<input id="person:name" name="name" type="hidden" value="Jim" />'
        assert self.m.hidden("name") == b

    def test_password_field(self):
        b = '<input id="person:name" name="name" type="password" value="Jim" />'
        assert self.m.password("name") == b

    def test_file_field(self):
        b = '<input id="person:name" name="name" type="file" value="Jim" />'
        assert self.m.file("name") == b

    def test_radio_button(self):
        b = '<input checked="checked" id="person:favcolor_blue" name="favcolor" type="radio" value="blue" />'
        assert self.m.radio("favcolor", "blue") == b

    def test_radio_button2(self):
        b = '<input id="person:favcolor_red" name="favcolor" type="radio" value="red" />'
        assert self.m.radio("favcolor", "red") == b

    def test_text_area(self):
        b = '<textarea id="person:longtext" name="longtext">lorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\nlorem ipsum lorem ipsum\n</textarea>'
        assert self.m.textarea("longtext") == b

    def test_text_field(self):
        b = '<input id="person:name" name="name" type="text" value="Jim" />'
        assert self.m.text("name") == b

    def test_select(self):
        a = self.m.select("lang", [("en", "English"), ("de", "German"), ("jp", "Japanese")])
        b = '<select id="person:lang" name="lang">\n<option selected="selected" value="en">English</option>\n<option value="de">German</option>\n<option value="jp">Japanese</option>\n</select>'
        assert a == b


class TestModelTagsHelperWithoutObject(object):
    def setup_method(self, method):
        obj = ""
        self.m = ModelTags(obj)
        
    def test_check_box(self):
        b = '<input id="fulltime" name="fulltime" type="checkbox" value="1" />'
        assert self.m.checkbox("fulltime") == b

    def test_hidden_field(self):
        b = '<input id="name" name="name" type="hidden" value="" />'
        assert self.m.hidden("name") == b

    def test_password_field(self):
        b = '<input id="name" name="name" type="password" value="" />'
        assert self.m.password("name") == b

    def test_file_field(self):
        b = '<input id="name" name="name" type="file" value="" />'
        assert self.m.file("name") == b

    def test_radio_button(self):
        b = '<input id="favcolor_blue" name="favcolor" type="radio" value="blue" />'
        assert self.m.radio("favcolor", "blue") == b
        
    def test_radio_button2(self):
        b = '<input id="favcolor_red" name="favcolor" type="radio" value="red" />'
        assert self.m.radio("favcolor", "red") == b

    def test_text_area(self):
        b = '<textarea id="longtext" name="longtext"></textarea>'
        assert self.m.textarea("longtext") == b

    def test_text_field(self):
        b = '<input id="name" name="name" type="text" value="" />'
        assert self.m.text("name") == b

    def test_select(self):
        a = self.m.select("lang", [("en", "English"), ("de", "German"), ("jp", "Japanese")])
        b = '<select id="lang" name="lang">\n<option value="en">English</option>\n<option value="de">German</option>\n<option value="jp">Japanese</option>\n</select>'
        assert a == b

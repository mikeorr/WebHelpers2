from pytest import raises

from webhelpers2.html import literal

class HTMLTestCase(object):

    def check(self, result, control):
        assert result == control
        assert isinstance(result, literal)

    def check_fail(self, result, control):
        with raises(AssertionError):
            self.check(result, control)



#### Tests for objects in this module ####

class TestHTMLTestCase(HTMLTestCase):
    def test1(self):
        a = literal("Foo")
        b = "Foo"
        self.check(a, b)

    def test2(self):
        a = literal("Foo")
        b = "Bar"
        self.check_fail(a, b)

    def test3(self):
        a = "Foo"
        b = a
        self.check_fail(a, b)



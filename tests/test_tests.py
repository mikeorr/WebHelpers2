""" Tests for test helpers in webhelpers2.tests
"""

from webhelpers2.html import literal
from webhelpers2.tests import HTMLTestCase

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

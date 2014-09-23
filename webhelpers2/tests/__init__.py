from pytest import raises

from webhelpers2.html import literal

class HTMLTestCase(object):

    def check(self, result, control):
        assert result == control
        assert isinstance(result, literal)

    def check_fail(self, result, control):
        with raises(AssertionError):
            self.check(result, control)

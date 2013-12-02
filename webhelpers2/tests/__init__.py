from pytest import raises

class HTMLTestCase(object):

    def check(self, result, control):
        from webhelpers2.html import literal
        assert result == control
        assert isinstance(result, literal)

    def check_fail(self, result, control):
        with raises(AssertionError):
            self.check(result, control)

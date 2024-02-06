import pytest

from webhelpers2.misc import *

def test_choose_height():
    assert choose_height(400, 800, 600) == 300


def by_name(class_):
    return class_.__name__

def is_int(x):
    return isinstance(x, int)

class TestCountTrue(object):
    def test_count_true(self):
        assert count_true([1, 2, 0, "A", ""]) == 3

    def test_count_true2(self):
        assert count_true([1, "A", 2], is_int) == 2


class TestConvert(object):
    def test1(self):
        assert convert("5", int) == 5

    def test2(self):
        assert convert("A", int) == None


class TestFlatten(object):
    def test1(self):
        assert list(flatten([1, [2, 3], 4])) == [1, 2, 3, 4]

    def test2(self):
        assert list(flatten([1, (2, 3, [4]), 5])) == [1, 2, 3, 4, 5]
        

#### Simple test

class DummyBase(object):  pass
class Subclass1(DummyBase):  pass
class Subclass2(DummyBase):  pass

def test_subclasses_of():
    subclasses = subclasses_of(DummyBase, globals())
    subclasses.sort(key=by_name)
    control = [Subclass1, Subclass2]
    assert subclasses == control

#### Tea test

class Tea(object):  pass

# Abstract subclasses
class Black(Tea):  pass
class Green(Tea):  pass

# Concrete classes (grandchildren)
class EnglishBreakfast(Black):  pass
class Sencha(Green):  pass
class EarlGrey(Black):  pass
class JasminePearl(Green):  pass

def test_subclasses_of_with_exclude():
    subclasses = subclasses_of(Tea, globals(), [Black, Green])
    subclasses.sort(key=by_name)
    control = [EarlGrey, EnglishBreakfast, JasminePearl, Sencha]
    assert  subclasses == control


class TestFormatException(object):
    def test_with_explicit_exception(self):
        exc = ValueError('x')
        assert format_exception(exc) == 'ValueError: x'

    def test_from_exc_info(self):
        try:
            raise ValueError('foo')
        except:
            assert format_exception() == 'ValueError: foo'


class TestDeprecate(object):
    @pytest.mark.parametrize('pending, warning_class', [
        (False, DeprecationWarning),
        (True, PendingDeprecationWarning),
        ])
    def test_pending(self, pending, warning_class):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            deprecate('foo', pending=pending)
        assert len(w) == 1
        assert isinstance(w[0].message, warning_class)
        assert str(w[0].message) == 'foo'
        assert w[0].filename == __file__


class TestStudlyException(object):
    def test_static_message(self):
        class MyError(StudlyException):
            m = "can't frob the bar when foo is enabled"
        # Couldn't get pytest.raises to work here;
        # ``excinfo.value`` wasn't defined.
        try:
            raise MyError()
        except MyError as e:
            assert str(e) == "can't frob the bar when foo is enabled"
        else:
            raise AssertionError("didn't raise MyError")

    def test_message_with_keywords(self):
        class MyError(StudlyException):
            m = "can't frob the {bar} when {foo} is enabled"
        try:
            raise MyError(bar="baz", foo="food")
        except MyError as e:
            assert str(e) == "can't frob the baz when food is enabled"
            assert e.bar == "baz"
            assert e.foo == "food"
        else:
            raise AssertionError("didn't raise MyError")

    def test_default(self):
        try:
            raise StudlyException()
        except StudlyException as e:
            assert str(e) == ""
        else:
            raise AssertionError("didn't raise StudlyException")

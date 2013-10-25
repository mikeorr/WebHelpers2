from webhelpers2.misc import *

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

from pytest import raises

from webhelpers2.containers import *

food = ["apple", "banana", "carrot", "daikon", "egg", "fish", "gelato", "honey"]
food_extra = food + ["EXTRA"]

class TestDumbObject(object):
    def test1(self):
        do = DumbObject(a=1, b=2)
        assert do.b == 2


class TestCounter(object):
    def setup_method(self, method):
        self.counter = Counter()
        self.counter("foo")
        self.counter("bar")
        self.counter("foo")

    def test_result(self):
        assert sorted(self.counter.result.items()) == [("bar", 1), ("foo", 2)]

    def test_popular_limited(self):
        assert self.counter.get_popular(1) == [(2, "foo")]

    def test_popular(self):
        assert self.counter.get_popular() == [(2, "foo"), (1, "bar")]

    def test_sorted_items(self):
        assert self.counter.get_sorted_items() == [("bar", 1), ("foo", 2)]

    def test_corellate(self):
        c = Counter.correlate(["A", "B", "A"])
        assert c.result["A"] == 2
        assert c.result["B"] == 1


class TestDictFunctions(object):
    orig = {"A": 1, "B": 2, "C": 3}

    def test_copy_keys(self):
        assert copy_keys(self.orig, "A", "C") == {"A": 1, "C": 3}

    def test_copy_keys_except(self):
        assert copy_keys_except(self.orig, "A", "C") == {"B": 2}

    def test_split_dict(self):
        email_headers = {"From": "F", "To": "T", "Received": "R"}
        regular, extra = split_dict(email_headers, "To", "From")
        assert sorted(regular.keys()) == ["From", "To"]
        assert sorted(extra.keys()) == ["Received"]

    def test_split_dict_keyerror(self):
        with raises(KeyError):
            assert split_dict(self.orig, "Z") == {}, self.orig

    def test_ordered_items(self):
        email_headers = {}
        email_headers["To"] = "you"
        email_headers["From"] = "me"
        email_headers["Date"] = "2008/1/4"
        email_headers["Subject"] = "X"
        email_headers["Received"] = "..."
        order = ["From", "To", "Subject"]
        result = list(ordered_items(email_headers, order, False))
        assert result == [("From", "me"), ("To", "you"), ("Subject", "X")]

    def test_del_keys(self):
        d = self.orig.copy()
        del_keys(d, "A", "C")
        assert d == {"B": 2}

    def test_correlate_dicts(self):
        d1 = {"name": "Fred", "age": 41}
        d2 = {"name": "Barney", "age": 31}
        flintstones = correlate_dicts([d1, d2], "name")
        assert sorted(flintstones.keys()) == ["Barney", "Fred"]
        assert flintstones["Fred"]["age"] == 41

    def test_correlate_objects(self):
        class Flintstone(DumbObject):
            pass
        fred = Flintstone(name="Fred", age=41)
        barney = Flintstone(name="Barney", age=31)
        flintstones = correlate_objects([fred, barney], "name")
        assert sorted(flintstones.keys()) == ["Barney", "Fred"]
        assert flintstones["Barney"].age == 31


class TestDistribute(object):
    def test1(self):
        control = [
            ["apple", "banana", "carrot"], 
            ["daikon", "egg", "fish"], 
            ["gelato", "honey", ""]]
        assert distribute(food, 3, "H", "") == control

    def test2(self):
        control = [
            ["apple", "daikon", "gelato"], 
            ["banana", "egg", "honey"], 
            ["carrot", "fish", ""]]
        assert distribute(food, 3, "V", "") == control

    def test3(self):
        control = [
            ["apple", "banana"], 
            ["carrot", "daikon"], 
            ["egg", "fish"], 
            ["gelato", "honey"]]
        assert distribute(food, 2, "H", "") == control

    def test4(self):
        control = [
            ["apple", "egg"], 
            ["banana", "fish"], 
            ["carrot", "gelato"], 
            ["daikon", "honey"]]
        assert distribute(food, 2, "V", "") == control


class TestDistributeWithExtra(object):
    def test1(self):
        control = [
            ["apple", "banana", "carrot"], 
            ["daikon", "egg", "fish"], 
            ["gelato", "honey", "EXTRA"]]
        assert distribute(food_extra, 3, "H", "") == control

    def test2(self):
        control = [
            ["apple", "daikon", "gelato"], 
            ["banana", "egg", "honey"], 
            ["carrot", "fish", "EXTRA"]]
        assert distribute(food_extra, 3, "V", "") == control

    def test3(self):
        control = [
            ["apple", "banana"], 
            ["carrot", "daikon"], 
            ["egg", "fish"], 
            ["gelato", "honey"], 
            ["EXTRA", ""]]
        assert distribute(food_extra, 2, "H", "") == control

    def test4(self):
        control = [
            ["apple", "fish"], 
            ["banana", "gelato"], 
            ["carrot", "honey"], 
            ["daikon", "EXTRA"], 
            ["egg", ""]]
        assert distribute(food_extra, 2, "V", "") == control


class TestTranspose(object):
    def test1(self):
        a = transpose([["A", "B", "C"], ["D", "E", "F"]])
        b = [['A', 'D'], ['B', 'E'], ['C', 'F']]
        assert a == b

    def test2(self):
        a = transpose([["A", "B"], ["C", "D"], ["E", "F"]])
        b = [['A', 'C', 'E'], ['B', 'D', 'F']]
        assert a == b

    def test3(self):
        assert transpose([]) == []

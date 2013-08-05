from webhelpers2.containers import DumbObject
from webhelpers2.containers import distribute

food = ["apple", "banana", "carrot", "daikon", "egg", "fish", "gelato", "honey"]
food_extra = food + ["EXTRA"]

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

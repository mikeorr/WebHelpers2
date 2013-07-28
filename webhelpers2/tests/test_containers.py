# -*- coding: utf-8 -*-

from nose.tools import eq_

from util import raises

from webhelpers2.containers import DumbObject
from webhelpers2.containers import distribute

def test_distribute():
        food = ["apple", "banana", "carrot", "daikon", "egg", "fish", "gelato", "honey"]
        eq_(distribute(food, 3, "H", ""), [["apple", "banana", "carrot"], ["daikon", "egg", "fish"], ["gelato", "honey", ""]])
        eq_(distribute(food, 3, "V", ""), [["apple", "daikon", "gelato"], ["banana", "egg", "honey"], ["carrot", "fish", ""]])
        eq_(distribute(food, 2, "H", ""), [["apple", "banana"], ["carrot", "daikon"], ["egg", "fish"], ["gelato", "honey"]])
        eq_(distribute(food, 2, "V", ""), [["apple", "egg"], ["banana", "fish"], ["carrot", "gelato"], ["daikon", "honey"]])

def test_distribute_with_extra():
        food = ["apple", "banana", "carrot", "daikon", "egg", "fish", "gelato", "honey", "EXTRA"]
        eq_(distribute(food, 3, "H", ""), [["apple", "banana", "carrot"], ["daikon", "egg", "fish"], ["gelato", "honey", "EXTRA"]])
        eq_(distribute(food, 3, "V", ""), [["apple", "daikon", "gelato"], ["banana", "egg", "honey"], ["carrot", "fish", "EXTRA"]])
        eq_(distribute(food, 2, "H", ""), [["apple", "banana"], ["carrot", "daikon"], ["egg", "fish"], ["gelato", "honey"], ["EXTRA", ""]])
        eq_(distribute(food, 2, "V", ""), [["apple", "fish"], ["banana", "gelato"], ["carrot", "honey"], ["daikon", "EXTRA"], ["egg", ""]])

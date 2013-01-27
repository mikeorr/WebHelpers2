# -*- coding: utf-8 -*-

from nose.tools import eq_

from util import raises

from webhelpers2.containers import DumbObject
from webhelpers2.containers import distribute, get_many

def test_distribute():
        food = ["apple", "banana", "carrot", "daikon", "egg", "fish", "gelato", "honey"]
        eq_(distribute(food, 3, "H", ""), [['apple', 'banana', 'carrot'], ['daikon', 'egg', 'fish'], ['gelato', 'honey', '']])
        eq_(distribute(food, 3, "V", ""), [['apple', 'daikon', 'gelato'], ['banana', 'egg', 'honey'], ['carrot', 'fish', '']])
        eq_(distribute(food, 2, "H", ""), [['apple', 'banana'], ['carrot', 'daikon'], ['egg', 'fish'], ['gelato', 'honey']])
        eq_(distribute(food, 2, "V", ""), [['apple', 'egg'], ['banana', 'fish'], ['carrot', 'gelato'], ['daikon', 'honey']])

def test_distribute_with_extra():
        food = ["apple", "banana", "carrot", "daikon", "egg", "fish", "gelato", "honey", "EXTRA"]
        eq_(distribute(food, 3, "H", ""), [['apple', 'banana', 'carrot'], ['daikon', 'egg', 'fish'], ['gelato', 'honey', 'EXTRA']])
        eq_(distribute(food, 3, "V", ""), [['apple', 'daikon', 'gelato'], ['banana', 'egg', 'honey'], ['carrot', 'fish', 'EXTRA']])
        eq_(distribute(food, 2, "H", ""), [['apple', 'banana'], ['carrot', 'daikon'], ['egg', 'fish'], ['gelato', 'honey'], ['EXTRA', '']])
        eq_(distribute(food, 2, "V", ""), [['apple', 'fish'], ['banana', 'gelato'], ['carrot', 'honey'], ['daikon', 'EXTRA'], ['egg', '']])

def test_get_many():
    # Dict with keys and values of 0, 1, 2, 3, 4
    params = dict((n,n) for n in range(5))

    eq_(get_many(params), [])
    eq_(get_many(params, required=[1, 2]), [1, 2])
    eq_(get_many(params, optional=[1, 2]), [1, 2])
    eq_(get_many(params, optional=[6, 7, 8]), [None, None, None])
    eq_(get_many(params, one_of=[1, 2]), [1])
    eq_(get_many(params, one_of=[6, 1]), [1])

    eq_(get_many(params, optional=[6, 1]), [None, 1])
    eq_(get_many(params, required=[1, 2], optional=[6, 1]), [1, 2, None, 1])
    eq_(get_many(params, required=[1, 2], optional=[6, 1], one_of=[7, 8, 3]), [1, 2, None, 1, 3])

    raises(KeyError, get_many, params, required=[1, 6])
    raises(KeyError, get_many, params, one_of=[7, 6])

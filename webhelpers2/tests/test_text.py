# -*- coding: utf-8 -*-
from webhelpers2.text import *

class TestExcerptHelper(object):
    def test_excerpt(self):
        assert "...lo my wo..." == excerpt("hello my world", "my", 3)

    def test_excerpt2(self):
        assert "...is a beautiful morn..." == \
            excerpt("This is a beautiful morning", "beautiful", 5)

    def test_excerpt3(self):
        assert "This is a..." == excerpt("This is a beautiful morning", "this", 5)

    def test_excerpt4(self):
        assert "...iful morning" == excerpt("This is a beautiful morning", "morning", 5)

    def test_excerpt5(self):
        assert "" == excerpt("This is a beautiful morning", "day")

    def test_excerpt_with_regex(self):
        assert "...is a beautiful! mor..." == \
             excerpt("This is a beautiful! morning", "beautiful", 5)

    def test_excerpt_with_regex2(self):
        assert "...is a beautiful? mor..." == \
             excerpt("This is a beautiful? morning", "beautiful", 5)


class TestPluralHelper(object):
    def test1(self):
        assert plural(2, "ox", "oxen") == "2 oxen"

    def test2(self):
        assert plural(2, "ox", "oxen", False) == "oxen"


class TestChopHelper(object):
    def test_chop_at(self):
        assert chop_at("plutocratic brats", "rat") == "plutoc"

    def test_chop_at2(self):
        assert chop_at("plutocratic brats", "rat", True) == "plutocrat"

    def test_lchop(self):
        assert lchop("##This is a comment.##", "##") == "This is a comment.##"

    def test_rchop(self):
        assert rchop("##This is a comment.##", "##") == "##This is a comment."


class TestSeriesHelper(object):
    def test1(self):
        assert series(["A", "B", "C"]) == "A, B, and C"

    def test2(self):
        assert series(["A", "B", "C"], "or") == "A, B, or C"

    def test3(self):
        assert series(["A", "B", "C"], strict_commas=False) == "A, B and C"

    def test4(self):
        assert series(["A", "B"]) == "A and B"

    def test5(self):
        assert series(["A"]) == "A"

    def test6(self):
        assert series([]) == ""


class TestTruncateHelper(object):
    def test_truncate(self):
        assert "Hello World!" == truncate("Hello World!", 12)

    def test_truncate2(self):
        assert "Hello Wor..." == truncate("Hello World!!", 12)

    def test_truncate3(self):
        assert "Hello..." == truncate("Hello World!!", 12, whole_word=True)


class TestStripLeadingWhitespaceHelper(object):
    def test_strip_leading_whitespace(self):
        s = "    def fn(x):\n        return x\n"
        control = "def fn(x):\nreturn x\n"
        assert control == strip_leading_whitespace(s)


# @@MO wrap_paragraphs untested.


class TestURLifyHelper(object):
    def test_urlify(self):
        s = "What is this? It is a car."
        control = "what-is-this%3F-it-is-a-car."
        assert urlify(s) == control

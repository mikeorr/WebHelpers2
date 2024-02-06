# -*- coding: utf-8 -*-

import textwrap

import pytest

from webhelpers2.text import *
from webhelpers2.html import literal

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

    def test_excerpt_null_text(self):
        assert excerpt("", "foo") == ""

    def test_excerpt_null_phrase(self):
        assert excerpt("foo", None) == "foo"

    def test_excerpt_literal(self):
        result = excerpt(literal('Some fine morning'), 'fine')
        assert isinstance(result, literal)
        assert result == 'Some fine morning'

class TestPluralHelper(object):
    def test1(self):
        assert plural(2, "ox", "oxen") == "2 oxen"

    def test2(self):
        assert plural(2, "ox", "oxen", False) == "oxen"

    def test_singular(self):
        assert plural(1, "ox", "oxen") == "1 ox"


class TestChopHelper(object):
    def test_chop_at(self):
        assert chop_at("plutocratic brats", "rat") == "plutoc"

    def test_chop_at2(self):
        assert chop_at("plutocratic brats", "rat", True) == "plutocrat"

    def test_chop_at_returns_whole_string_if_sub_not_found(self):
        assert chop_at("plutocratic brats", "wurst") == "plutocratic brats"

    def test_lchop(self):
        assert lchop("##This is a comment.##", "##") == "This is a comment.##"

    def test_rchop(self):
        assert rchop("##This is a comment.##", "##") == "##This is a comment."


class TestSeriesHelper(object):
    def test1(self):
        assert series("A", "B", "C") == "A, B, and C"

    def test2(self):
        assert series("A", "B", "C", conj="or") == "A, B, or C"

    def test3(self):
        assert series("A", "B", "C", strict=False) == "A, B and C"

    def test4(self):
        assert series("A", "B") == "A and B"

    def test5(self):
        assert series("A") == "A"

    def test6(self):
        assert series() == ""

    def test7(self):
        assert series("A", "B", "C", conj="or", strict=False) == "A, B or C"

    def test_type_error_on_unexpect_kwargs(self):
        with pytest.raises(TypeError):
            series("A", "B", arg='unexpected')

class TestTruncateHelper(object):
    def test_truncate(self):
        assert "Hello World!" == truncate("Hello World!", 12)

    def test_truncate2(self):
        assert "Hello Wor..." == truncate("Hello World!!", 12)

    def test_truncate3(self):
        assert "Hello..." == truncate("Hello World!!", 12, whole_word=True)

    def test_truncate_none(self):
        assert truncate(None) == ""

    def test_truncate_long_whole_word(self):
        assert truncate("Hello World!!", 6, whole_word=True) == "Hel..."


class TestStripLeadingWhitespaceHelper(object):
    def test_strip_leading_whitespace(self):
        s = "    def fn(x):\n        return x\n"
        control = "def fn(x):\nreturn x\n"
        assert control == strip_leading_whitespace(s)


class TestWrapLongLinesHelper(object):
    def test_all_short_lines(self):
        s = "short\nshort short\nshort short\nshort short\n"
        control = "short\nshort short\nshort short\nshort short\n"
        assert wrap_long_lines(s, 11) == control

    def test_long_line_in_middle(self):
        s = "short\nshort short\nlong long long\nshort short\n"
        control = "short\nshort short\nlong long\nlong\nshort short\n"
        assert wrap_long_lines(s, 11) == control

    def test_with_textwrapper(self):
        paragraph = 'word ' * 7 + 'word\n\n'
        wrapped = 'word word\n' * 4 + '\n'
        width = textwrap.TextWrapper(width=10)
        assert wrap_long_lines(paragraph * 2, width) == wrapped * 2


class TestWrapParagraphsHelper(object):
    def test(self):
        paragraph = 'word word word word\n' * 2 + '\n'
        wrapped = 'word word\n' * 4 + '\n'
        assert wrap_paragraphs(paragraph * 2, 10) == wrapped * 2

    def test_short_lines(self):
        paragraph = 'word\n' * 8 + '\n'
        assert wrap_paragraphs(paragraph * 2, 10) == paragraph * 2

    def test_with_textwrapper(self):
        paragraph = 'word ' * 7 + 'word\n\n'
        wrapped = 'word word\n' * 4 + '\n'
        width = textwrap.TextWrapper(width=10)
        assert wrap_paragraphs(paragraph * 2, width) == wrapped * 2

class TestURLifyHelper(object):
    def test_urlify(self):
        s = "What is this? It is a car."
        control = "what-is-this%3F-it-is-a-car."
        assert urlify(s) == control

    def test_urlify_calls_unidecode(self, monkeypatch):
        from webhelpers2 import text
        monkeypatch.setattr(text, 'unidecode', lambda s: 'unidecoded')
        assert urlify('foo') == 'unidecoded'

# -*- coding: utf-8 -*-
from webhelpers2.text import *

class TestTextHelper(object):
    
    def test_excerpt(self):
        assert "...lo my wo..." == excerpt("hello my world", "my", 3)
        assert "...is a beautiful morn..." == \
            excerpt("This is a beautiful morning", "beautiful", 5)
        assert "This is a..." == excerpt("This is a beautiful morning", "this", 5)
        assert "...iful morning" == excerpt("This is a beautiful morning", "morning", 5)
        assert "" == excerpt("This is a beautiful morning", "day")

    def test_excerpt_with_regex(self):
        assert "...is a beautiful! mor..." == \
             excerpt("This is a beautiful! morning", "beautiful", 5)
        assert "...is a beautiful? mor..." == \
             excerpt("This is a beautiful? morning", "beautiful", 5)

    def test_excerpt_with_utf8(self):
        assert u"...ﬃciency could not be ..." == \
             excerpt(u"That's why eﬃciency could not be helped", "could", 8)


    def test_truncate(self):
        assert "Hello World!" == truncate("Hello World!", 12)
        assert "Hello Wor..." == truncate("Hello World!!", 12)
        assert "Hello..." == truncate("Hello World!!", 12, whole_word=True)

    def test_strip_leading_whitespace(self):
        s = "    def fn(x):\n        return x\n"
        control = "def fn(x):\nreturn x\n"
        assert control == strip_leading_whitespace(s)

    # @@MO wrap_paragraphs untested.

    def test_urlify(self):
        s = "What is this? It is a car."
        control = "What%20is%20this%3f%20It%20is%20a%20car."

# -*- coding: utf-8 -*-
from nose.tools import eq_

from webhelpers2.html import HTML, literal
from webhelpers2.html.converters import *

def test_nl2br():
    eq_(u'A B<br />\nC D<br />\n<br />\nE F', nl2br("A B\nC D\r\n\r\nE F"))

def test_nl2br2():
    eq_(u'&lt;strike&gt;W&lt;/strike&gt;<br />\nThe W', nl2br("<strike>W</strike>\nThe W"))

def test_nl2br3():
    eq_(u'<strike>W</strike><br />\nThe W', nl2br(literal("<strike>W</strike>\nThe W")))

def test_format_paragraphs1():
    eq_(u"<p>crazy\n cross\n platform linebreaks</p>", format_paragraphs("crazy\r\n cross\r platform linebreaks"))

def test_format_paragraphs2():
    eq_(u"<p>crazy<br />\n cross<br />\n platform linebreaks</p>", format_paragraphs("crazy\r\n cross\r platform linebreaks", True))

def test_format_paragraphs3():
    eq_(u"<p>A paragraph</p>\n\n<p>and another one!</p>", format_paragraphs("A paragraph\n\nand another one!"))

def test_format_paragraphs4():
    eq_(u"<p>A paragraph<br />\n With a newline</p>", format_paragraphs("A paragraph\n With a newline", True))

def test_format_paragraphs5():
    eq_(u"<p>A paragraph\n With a newline</p>", format_paragraphs("A paragraph\n With a newline", False))

def test_format_paragraphs6():
    eq_(u"<p>A paragraph\n With a newline</p>", format_paragraphs("A paragraph\n With a newline"))

def test_format_paragraphs7():
    eq_(u"", format_paragraphs(None))

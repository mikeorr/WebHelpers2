# -*- coding: utf-8 -*-

# This module remains ``tests/test_converters.py`` even though the helpers have
# moved to ``webhelpers.html.tools``, pending a general tests overhaul.

from nose.tools import eq_

from webhelpers2.html import HTML, literal
from webhelpers2.html.tools import *

def test_nl2br():
    eq_(u"A B<br />\nC D<br />\n<br />\nE F", nl2br("A B\nC D\r\n\r\nE F"))

def test_nl2br2():
    eq_(u"&lt;strike&gt;W&lt;/strike&gt;<br />\nThe W", nl2br("<strike>W</strike>\nThe W"))

def test_nl2br3():
    eq_(u"<strike>W</strike><br />\nThe W", nl2br(literal("<strike>W</strike>\nThe W")))

def test_text_to_html1():
    eq_(u"<p>crazy\n cross\n platform linebreaks</p>", text_to_html("crazy\r\n cross\r platform linebreaks"))

def test_text_to_html2():
    eq_(u"<p>crazy<br />\n cross<br />\n platform linebreaks</p>", text_to_html("crazy\r\n cross\r platform linebreaks", True))

def test_text_to_html3():
    eq_(u"<p>A paragraph</p>\n\n<p>and another one!</p>", text_to_html("A paragraph\n\nand another one!"))

def test_text_to_html4():
    eq_(u"<p>A paragraph<br />\n With a newline</p>", text_to_html("A paragraph\n With a newline", True))

def test_text_to_html5():
    eq_(u"<p>A paragraph\n With a newline</p>", text_to_html("A paragraph\n With a newline", False))

def test_text_to_html6():
    eq_(u"<p>A paragraph\n With a newline</p>", text_to_html("A paragraph\n With a newline"))

def test_text_to_html7():
    eq_(u"", text_to_html(None))

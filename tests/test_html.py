from __future__ import unicode_literals

from nose.tools import eq_

from webhelpers2.html import literal, lit_sub, escape, HTML

def test_double_escape():
    quoted = escape('This string is "quoted"')
    eq_(quoted, 'This string is &#34;quoted&#34;')
    dbl_quoted = escape(quoted)
    eq_(quoted, dbl_quoted)

def test_literal():
    lit = literal('This string <>')
    other = literal('<other>')
    eq_('This string <><other>', lit + other)
    assert type(lit + other) is literal
    
    eq_('&#34;<other>', '"' + other)
    eq_('<other>&#34;', other + '"')
    
    mod = literal('<%s>ello')
    eq_('<&lt;H&gt;>ello', mod % '<H>')
    assert type(mod % '<H>') is literal
    eq_(HTML('<a>'), '&lt;a&gt;')
    assert type(HTML('<a>')) is literal

def test_literal_dict():
    lit = literal('This string <>')
    unq = 'This has <crap>'
    sub = literal('%s and %s')
    eq_('This string <> and This has &lt;crap&gt;', sub % (lit, unq))
    
    sub = literal('%(lit)s and %(lit)r')
    #eq_("This string <> and literal(u&#39;This string &lt;&gt;&#39;)", sub % dict(lit=lit))
    sub = literal('%(unq)r and %(unq)s')
    eq_("&#39;This has &lt;crap&gt;&#39; and This has &lt;crap&gt;", sub % dict(unq=unq))

def test_literal_mul():
    lit = literal('<>')
    eq_('<><><>', lit * 3)
    assert isinstance(lit*3, literal)

def test_literal_join():
    lit = literal('<>')
    assert isinstance(lit.join(['f', 'a']), literal)
    eq_('f<>a', lit.join(('f', 'a')))

def test_literal_int():
    lit = literal('<%i>')
    eq_('<5>', lit % 5)

def test_html():
    a = HTML.a(href='http://mostlysafe\" <tag', c="Bad <script> tag")
    eq_(a, '<a href="http://mostlysafe&#34; &lt;tag">Bad &lt;script&gt; tag</a>')
    
    img = HTML.img(src='http://some/image.jpg')
    eq_(img, '<img src="http://some/image.jpg" />')
    
    br = HTML.br()
    eq_('<br />', br)

def test_lit_re():
    lit = literal('This is a <string>')
    unlit = 'This is also a <string>'
    
    result = lit_sub(r'<str', literal('<b'), lit)
    eq_('This is a <bing>', escape(result))
    
    result = lit_sub(r'a <str', 'a <b> <b', unlit)
    eq_('This is also a &lt;b&gt; &lt;bing&gt;', escape(result))

def test_unclosed_tag():
    result = HTML.form(_closed=False)
    print(result)
    eq_('<form>', result)
    
    result = HTML.form(_closed=False, action="hello")
    eq_('<form action="hello">', result)

def test_newline_arg():
    eq_(HTML.a(),         literal('<a></a>'))
    eq_(HTML.a(_nl=True), literal('<a>\n</a>\n'))
    eq_(HTML.a(_closed=False),           literal('<a>'))
    eq_(HTML.a(_closed=False, _nl=True), literal('<a>\n'))
    eq_(HTML.a("A", "B", href="/"),      literal('<a href="/">AB</a>'))
    eq_(HTML.a("A", "B", href="/", _nl=True), literal('<a href="/">\nA\nB\n</a>\n'))

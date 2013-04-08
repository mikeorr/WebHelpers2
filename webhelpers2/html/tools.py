"""HTML helpers that are more than just simple tags.

I contain helpers to generate complex tags, to convert text to HTML, and to strip
tags.

There are no helpers to prettify HTML or canonicalize whitespace because
BeautifulSoup and HTMLTidy handle this well.
"""

import re
import urllib

from webhelpers2.html._autolink import auto_link
from webhelpers2.html._render import html_to_text, sanitize
from webhelpers2.html import HTML, literal, lit_sub, escape
import webhelpers2.html.tags as tags

__all__ = [
    "auto_link", 
    "button_to", 
    "html_to_text",
    "js_obfuscate",
    "highlight", 
    "mail_to",
    "nl2br",
    "sanitize",
    "strip_links",
    "strip_tags",
    "text_to_html",
    ]

tag_re = re.compile(r'<.*?>', re.S)
br_re = re.compile(r'<br.*?>', re.I|re.S)
comment_re = re.compile(r'<!--|-->')

_universal_newline_rx = re.compile(R"\r\n|\n|\r")  # All types of newline.
_paragraph_rx = re.compile(R"\n{2,}")  # Paragraph break: 2 or more newlines.
br = HTML.br() + "\n"


def button_to(name, url='', **html_attrs):
    """Generate a form containing a sole button that submits to
    ``url``. 
    
    Use this method instead of ``link_to`` for actions that do not have
    the safe HTTP GET semantics implied by using a hypertext link.
    
    The parameters are the same as for ``link_to``.  Any 
    ``html_attrs`` that you pass will be applied to the inner
    ``input`` element. In particular, pass
    
        disabled = True/False
    
    as part of ``html_attrs`` to control whether the button is
    disabled.  The generated form element is given the class
    'button-to', to which you can attach CSS styles for display
    purposes.
    
    The submit button itself will be displayed as an image if you 
    provide both ``type`` and ``src`` as followed:

         type='image', src='icon_delete.gif'

    The ``src`` path should be the exact URL desired.  A previous version of
    this helper added magical prefixes but this is no longer the case.

    Example 1::
    
        # inside of controller for "feeds"
        >> button_to("Edit", url(action='edit', id=3))
        <form method="post" action="/feeds/edit/3" class="button-to">
        <div><input value="Edit" type="submit" /></div>
        </form>
    
    Example 2::
    
        >> button_to("Destroy", url(action='destroy', id=3), 
        .. method='DELETE')
        <form method="POST" action="/feeds/destroy/3" 
         class="button-to">
        <div>
            <input type="hidden" name="_method" value="DELETE" />
            <input value="Destroy" type="submit" />
        </div>
        </form>

    Example 3::

        # Button as an image.
        >> button_to("Edit", url(action='edit', id=3), type='image', 
        .. src='icon_delete.gif')
        <form method="POST" action="/feeds/edit/3" class="button-to">
        <div><input alt="Edit" src="/images/icon_delete.gif"
         type="image" value="Edit" /></div>
        </form>
    
    .. note::
        This method generates HTML code that represents a form. Forms
        are "block" content, which means that you should not try to
        insert them into your HTML where only inline content is
        expected. For example, you can legally insert a form inside of
        a ``div`` or ``td`` element or in between ``p`` elements, but
        not in the middle of a run of text, nor can you place a form
        within another form.
        (Bottom line: Always validate your HTML before going public.)

    Changed in WebHelpers 1.2: Preserve case of "method" arg for XHTML
    compatibility. E.g., "POST" or "PUT" causes *method="POST"*; "post" or
    "put" causes *method="post"*.
    
    """
    if html_attrs:
        tags.convert_boolean_attrs(html_attrs, ['disabled'])
    
    method_tag = ''
    method = html_attrs.pop('method', '')
    if method.upper() in ['PUT', 'DELETE']:
        method_tag = HTML.input(
            type='hidden', id='_method', name_='_method', value=method)
  
    if method.upper() in ('GET', 'POST'):
        form_method = method
    elif method in ('put', 'delete'):
        # preserve lowercasing of verb
        form_method = 'post'
    else:
        form_method = 'POST'
    
    url, name = url, name or url
    
    submit_type = html_attrs.get('type')
    img_source = html_attrs.get('src')
    if submit_type == 'image' and img_source:
        html_attrs["value"] = name
        html_attrs.setdefault("alt", name)
    else:
        html_attrs["type"] = "submit"
        html_attrs["value"] = name
    
    return HTML.form(method=form_method, action=url, class_="button-to",
                     c=[HTML.div(method_tag, HTML.input(**html_attrs))])

def js_obfuscate(content):
    """Obfuscate data in a Javascript tag.
    
    Example::
        
        >>> js_obfuscate("<input type='hidden' name='check' value='valid' />")
        literal(u'<script type="text/javascript">\\n//<![CDATA[\\neval(unescape(\\'%64%6f%63%75%6d%65%6e%74%2e%77%72%69%74%65%28%27%3c%69%6e%70%75%74%20%74%79%70%65%3d%27%68%69%64%64%65%6e%27%20%6e%61%6d%65%3d%27%63%68%65%63%6b%27%20%76%61%6c%75%65%3d%27%76%61%6c%69%64%27%20%2f%3e%27%29%3b\\'))\\n//]]>\\n</script>')
        
    """
    doc_write = "document.write('%s');" % content
    obfuscated = ''.join(['%%%x' % ord(x) for x in doc_write])
    complete = "eval(unescape('%s'))" % obfuscated
    cdata = HTML.cdata("\n", complete, "\n//")
    return HTML.script("\n//", cdata, "\n", type="text/javascript")


def mail_to(email_address, name=None, cc=None, bcc=None, subject=None, 
    body=None, replace_at=None, replace_dot=None, encode=None, **html_attrs):
    """Create a link tag for starting an email to the specified 
    ``email_address``.
    
    This ``email_address`` is also used as the name of the link unless
    ``name`` is specified. Additional HTML options, such as class or
    id, can be passed in the ``html_attrs`` hash.
    
    You can also make it difficult for spiders to harvest email address
    by obfuscating them.
    
    Examples::
    
        >>> mail_to("me@domain.com", "My email", encode = "javascript")
        literal(u'<script type="text/javascript">\\n//<![CDATA[\\neval(unescape(\\'%64%6f%63%75%6d%65%6e%74%2e%77%72%69%74%65%28%27%3c%61%20%68%72%65%66%3d%22%6d%61%69%6c%74%6f%3a%6d%65%40%64%6f%6d%61%69%6e%2e%63%6f%6d%22%3e%4d%79%20%65%6d%61%69%6c%3c%2f%61%3e%27%29%3b\\'))\\n//]]>\\n</script>')
    
        >>> mail_to("me@domain.com", "My email", encode = "hex")
        literal(u'<a href="&#109;&#97;&#105;&#108;&#116;&#111;&#58;%6d%65@%64%6f%6d%61%69%6e.%63%6f%6d">My email</a>')
    
    You can also specify the cc address, bcc address, subject, and body
    parts of the message header to create a complex e-mail using the 
    corresponding ``cc``, ``bcc``, ``subject``, and ``body`` keyword 
    arguments. Each of these options are URI escaped and then appended
    to the ``email_address`` before being output. **Be aware that 
    javascript keywords will not be escaped and may break this feature 
    when encoding with javascript.**
    
    Examples::
    
        >>> mail_to("me@domain.com", "My email", cc="ccaddress@domain.com", bcc="bccaddress@domain.com", subject="This is an example email", body= "This is the body of the message.")
        literal(u'<a href="mailto:me@domain.com?cc=ccaddress%40domain.com&amp;bcc=bccaddress%40domain.com&amp;subject=This%20is%20an%20example%20email&amp;body=This%20is%20the%20body%20of%20the%20message.">My email</a>')
        
    """
    extras = []
    for item in ('cc', cc), ('bcc', bcc), ('subject', subject), ('body', body):
        option = item[1]
        if option:
            if not isinstance(option, literal):
                item = (item[0], escape(option))
            extras.append(item)
    options_query = urllib.urlencode(extras).replace("+", "%20")
    protocol = 'mailto:'

    email_address_obfuscated = email_address
    if replace_at:
        email_address_obfuscated = email_address_obfuscated.replace('@', 
            replace_at)
    if replace_dot:
        email_address_obfuscated = email_address_obfuscated.replace('.', 
            replace_dot)

    if encode == 'hex':
        email_address_obfuscated = HTML.literal(''.join(
            ['&#%d;' % ord(x) for x in email_address_obfuscated]))
        protocol = HTML.literal(''.join(['&#%d;' % ord(x) for x in protocol]))

        word_re = re.compile('\w')
        encoded_parts = []
        for x in email_address:
            if word_re.match(x):
                encoded_parts.append('%%%x' % ord(x))
            else:
                encoded_parts.append(x)
        email_address = HTML.literal(''.join(encoded_parts))

    url = HTML.literal(protocol + email_address)
    if options_query:
        url += HTML.literal('?') + options_query
    html_attrs['href'] = url

    tag = HTML.a(name or email_address_obfuscated, **html_attrs)

    if encode == 'javascript':
        tmp = "document.write('%s');" % tag
        string = ''.join(['%%%x' % ord(x) for x in tmp])
        return HTML.script(
            HTML.literal("\n//<![CDATA[\neval(unescape('%s'))\n//]]>\n" % string),
                         type="text/javascript")
    else:
        return tag



def highlight(text, phrase, case_sensitive=False, class_="highlight", **attrs):
    """Highlight all occurrences of ``phrase`` in ``text``.

    This inserts "<strong class="highlight">...</strong>" around every
    occurrence.

    Arguments:
    
    ``text``: 
        The full text.
    
    ``phrase``: 
        A phrase to find in the text. This may be a string, a list of strings, 
        or a compiled regular expression. If a string, it's regex-escaped and
        compiled. If a list, all of the strings will be highlighted.  This is
        done by regex-escaping all elements and then joining them using the
        regex "|" token.

    ``case_sensitive``:
        If false (default), the phrases are searched in a case-insensitive
        manner. No effect if ``phrase`` is a regex object.

    ``class_``:
        CSS class for the <strong> tag.

    ``**attrs``:
        Additional HTML attributes for the <strong> tag.
    """
    if not phrase or not text:
        return text
    text = escape(text)
    if case_sensitive:
        flags = 0   # No flags.
    else:
        flags = re.IGNORECASE
    if isinstance(phrase, basestring):
        pat = re.escape(phrase)
        rx = re.compile(pat, flags)
    elif isinstance(phrase, (list, tuple)):
        parts = [re.escape(x) for x in phrase]
        pat = "|".join(parts)
        rx = re.compile(pat, flags)
    else:
        rx = phrase
    def repl(m):
        return HTML.strong(m.group(), class_=class_, **attrs)
    return lit_sub(rx, repl, text)

def strip_links(text):
    """
    Strip link tags from ``text`` leaving just the link label.
    
    Example::
    
        >>> strip_links('<a href="something">else</a>')
        'else'
        
    """
    if isinstance(text, literal):
        lit = literal
    else:
        lit = lambda x: x
    strip_re = re.compile(r'<a\b.*?>(.*?)<\/a>', re.I | re.M)
    return lit(strip_re.sub(r'\1', text))

def strip_tags(text):
    """Delete any HTML tags in the text, leaving their contents intact.
    Convert newlines to spaces, and <br /> to newlines.

    Example::
        >>> strip_tags('Text <em>emphasis</em> <script>Javascript</script>.')
        'Text emphasis Javascript.'
        >>> strip_tags('Ordinary <!-- COMMENT! --> text.')
        'Ordinary  COMMENT!  text.'
        >>> strip_tags('Line\\n1<br />Line 2')
        'Line 1\\nLine 2'

    Implementation copied from ``WebOb``.

    ``sanitize()`` does almost the same thing, but has a different
    implementation.
    """
    text = text.replace('\n', ' ')
    text = text.replace('\r', '')
    text = br_re.sub('\n', text)
    text = comment_re.sub('', text)
    text = tag_re.sub('', text)
    return text


def nl2br(text):
    """Insert a <br /> before each newline.
    """
    if text is None:
        return literal("")
    text = lit_sub(_universal_newline_rx, "\n", text)
    text = HTML(text).replace("\n", br)
    return text

def text_to_html(text, preserve_lines=False):
    """Convert text to HTML paragraphs.

    ``text``:
        the text to convert.  Split into paragraphs at blank lines (i.e.,
        wherever two or more consecutive newlines appear), and wrap each
        paragraph in a <p>.

    ``preserve_lines``:
        If true, add <br />  before each single line break
    """
    if text is None:
        return literal("")
    text = lit_sub(_universal_newline_rx, "\n", text)
    paragraphs = _paragraph_rx.split(text)
    for i, para in enumerate(paragraphs):
        if preserve_lines:
            para = HTML(para)
            para = para.replace("\n", br)
        paragraphs[i] = HTML.p(para)
    return literal("\n\n").join(paragraphs)


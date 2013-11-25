"""Implementation of ``auto_link()`` helper.
"""

from __future__ import unicode_literals
import re

from webhelpers2.html import HTML, literal, lit_sub, escape

__all__ = ["auto_link"]

AUTO_LINK_RE = re.compile(r"""
                        (                          # leading text
                          <\w+.*?>|                # leading HTML tag, or
                          [^=!:'"/]|               # leading punctuation, or 
                          ^                        # beginning of line
                        )
                        (
                          (?:https?://)|           # protocol spec, or
                          (?:www\.)                # www.*
                        ) 
                        (
                          [-\w]+                   # subdomain or domain
                          (?:\.[-\w]+)*            # remaining subdomains or domain
                          (?::\d+)?                # port
                          (?:/(?:(?:[~\w\+%-]|(?:[,.;:][^\s$]))+)?)* # path
                          (?:\?[\w\+\/%&=.;-]+)?     # query string
                          (?:\#[\w\-]*)?           # trailing anchor
                        )
                        ([\.,"'?!;:]|\s|<|\]|$)       # trailing text
                           """, re.X)


def auto_link(text, link="all", **href_attrs):
    """
    Turn all urls and email addresses into clickable links.
    
    ``link``
        Used to determine what to link. Options are "all", 
        "email_addresses", or "urls"

    ``href_attrs``
        Additional attributes for generated <a> tags.
    
    Example::
    
        >>> auto_link("Go to http://www.planetpython.com and say hello to guido@python.org")
        literal(u'Go to <a href="http://www.planetpython.com">http://www.planetpython.com</a> and say hello to <a href="mailto:guido@python.org">guido@python.org</a>')
        
    """
    if not text:
        return literal("")
    text = escape(text)
    if link == "all":
        return _auto_link_urls(_auto_link_email_addresses(text), **href_attrs)
    elif link == "email_addresses":
        return _auto_link_email_addresses(text)
    else:
        return _auto_link_urls(text, **href_attrs)

def _auto_link_urls(text, **href_attrs):
    def handle_match(matchobj):
        all = matchobj.group()
        before, prefix, link, after = matchobj.group(1, 2, 3, 4)
        if re.match(r'<a\s', before, re.I):
            return all
        text = literal(prefix + link)
        if prefix == "www.":
            prefix = "http://www."
        a_options = dict(href_attrs)
        a_options['href'] = literal(prefix + link)
        return literal(before) + HTML.a(text, **a_options) + literal(after)
    return literal(re.sub(AUTO_LINK_RE, handle_match, text))

def _auto_link_email_addresses(text):
    return lit_sub(r'([\w\.!#\$%\-+.]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)+)',
                   literal(r'<a href="mailto:\1">\1</a>'), text)

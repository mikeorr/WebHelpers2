"""Utility functions used by various web helpers.

This module contains support functions used by other helpers, and functions for
URL manipulation. Most of these helpers predate the 0.6 reorganization; they
would have been put in other subpackages if they have been created later.
"""
import urllib
import urlparse

def update_params(_url, _debug=False, **params):
    """Update query parameters in a URL.

    ``_url`` is any URL, with or without a query string.

    ``\*\*params`` are query parameters to add or replace. Each value may be a
    string, a list of strings, or None. Passing a list generates multiple
    values for the same parameter. Passing None deletes the corresponding
    parameter if present.

    Return the new URL.

    *Debug mode:* if a pseudo-parameter ``_debug=True`` is passed,
    return a tuple: ``[0]`` is the URL without query string or fragment,
    ``[1]`` is the final query parameters as a dict, and ``[2]`` is the
    fragment part of the original URL or the empty string.

    Usage:

    >>> update_params("foo", new1="NEW1")
    'foo?new1=NEW1'
    >>> update_params("foo?p=1", p="2")
    'foo?p=2'
    >>> update_params("foo?p=1", p=None)
    'foo'
    >>> update_params("http://example.com/foo?new1=OLD1#myfrag", new1="NEW1")
    'http://example.com/foo?new1=NEW1#myfrag'
    >>> update_params("http://example.com/foo?new1=OLD1#myfrag", new1="NEW1", _debug=True)
    ('http://example.com/foo', {'new1': 'NEW1'}, 'myfrag')
    >>> update_params("http://www.mau.de?foo=2", brrr=3)
    'http://www.mau.de?foo=2&brrr=3'
    >>> update_params("http://www.mau.de?foo=A&foo=B", foo=["C", "D"])
    'http://www.mau.de?foo=C&foo=D'

    """
    url, fragment = urlparse.urldefrag(_url)
    if "?" in url:
        url, qs = url.split("?", 1)
        query = urlparse.parse_qs(qs)
    else:
        query = {}
    for key, value in params.iteritems():
        if value is not None:
            query[key] = value
        elif key in query:
            del query[key]
    if _debug:
        return url, query, fragment
    qs = urllib.urlencode(query, True)
    if qs:
        qs = "?" + qs
    if fragment:
        fragment = "#" + fragment
    return "%s%s%s" % (url, qs, fragment)

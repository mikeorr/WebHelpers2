# -*- coding: utf-8 -*-
""" Check that lists of special names against the HTML specification.

These tests scrape the on-line HTML5 and HTML4 specifications to check
that the lists of empty elements, boolean attributes, and list- or
set-valued attributes (in ``HTML.void_tags``, ``HTML.boolean_attrs``,
and ``HTML.compose_attrs``, respectively) are in sync with the spec.

Notes
=====

Since the name of this module does not start with ``test_``, it
will not normally be collected by ``py.test``[*]_.  To run it,
try::

   path/to/py.test webhelpers2/tests/check_html_spec.py

Also note that these tests require the ``beautifulsoup4`` package to
be installed.

"""
from collections import namedtuple
import re

import pytest
from six.moves.urllib.request import urlopen
from webhelpers2.html.builder import literal, HTML

try:
    from bs4 import BeautifulSoup
except ImportError:
    pytest.skip("beautifulsoup4 is not installed")


# Most recent published HTML 5.1 working draft
HTML51_INDEX = "http://www.w3.org/TR/html51/fullindex.html"

# HTML 4.01 table of elements
HTML401_ELEMENTS = "http://www.w3.org/TR/html401/index/elements.html"


def test_void_tags(html5_element_table, html4_element_table):
    html5_empty_tags = set(row.element
                           for row in html5_element_table
                           if row.children == 'empty')
    assert 'br' in html5_empty_tags, "scraped results do not look sane"

    html4_empty_tags = set(row.name.lower()
                           for row in html4_element_table
                           if row.empty == 'E')
    assert 'br' in html4_empty_tags, "scraped results do not look sane"

    control = html5_empty_tags | html4_empty_tags
    control.discard("iframe")     # Not empty.
    control.discard("template")   # Not empty.

    void_tags = set(HTML.void_tags)
    void_tags.discard("keygen")     # Removed from HTML 5.
    void_tags.discard("menuitem")   # Removed from HTML 5.

    assert void_tags == control


def test_boolean_attrs(html5_attribute_table):
    html5_boolean_attrs = set(row.attribute
                              for row in html5_attribute_table
                              if row.value == 'Boolean attribute')
    assert 'selected' in html5_boolean_attrs, \
        "scraped results do not look sane"

    html5_boolean_attrs.add("hidden")   # Boolean-compatible attr.

    boolean_attrs = set(HTML.boolean_attrs)
    boolean_attrs.discard("typemustmatch")   # Removed from HTML 5.

    assert boolean_attrs == html5_boolean_attrs


def test_compose_attrs(html5_attribute_table):
    separators = [
        ('space-separated', ' '),
        ('comma-separated', ', '),
        ('list of integers', ','),
        ('list of floating-point numbers', ','),
        ('media query list', ', '),
        ('css declarations', '; '),
        ]
    html5_compose_attrs = {}
    for row in html5_attribute_table:
        value = row.value.lower()
        for description, separator in separators:
            if description in value:
                html5_compose_attrs[row.attribute] = literal(separator)
                break
    assert html5_compose_attrs['style'] == literal('; '), \
        "scraped results do not look sane"
    assert html5_compose_attrs['class'] == literal(' '), \
        "scraped results do not look sane"

    compose_attrs = HTML.compose_attrs.copy()
    del compose_attrs["accept-charset"]   # No longer a compose attr.
    del compose_attrs["dropzone"]         # Removed from HTML 5.
    del compose_attrs["rev"]              # Removed from HTML 5.

    assert compose_attrs == html5_compose_attrs


@pytest.fixture(scope='module')
def html5_index():
    resp = urlopen(HTML51_INDEX)
    return BeautifulSoup(resp, 'html5lib')


@pytest.fixture(scope='module')
def html5_element_table(html5_index):
    for table in html5_index.find_all('table'):
        if table.caption:
            caption = get_text(table.caption)
            if caption == 'List of elements':
                break
    else:
        raise RuntimeError("Can not find element table")
    return parse_table(table)


@pytest.fixture(scope='module')
def html5_attribute_table(html5_index):
    for table in html5_index.find_all('table'):
        if table.caption:
            caption = get_text(table.caption)
            if caption.startswith('List of attributes'):
                break
    else:
        raise RuntimeError("Can not find attribute table")
    return parse_table(table)


@pytest.fixture(scope='module')
def html4_element_table():
    # XXX: Some effort was put into parsing the HTML4 DTD directly to
    # extract the empty element list.  It appears that there is no
    # easy way to do this in python (without, e.g., writing a parser
    # oneself.)  (Note that the HTML4 DTD does not conform to the
    # XML1.0 DTD.)  Anyhow, it was decided that it was not worth the
    # effort.  (Since HTML4 is no longer evolving, any check of the
    # standard is probably overkill.)
    resp = urlopen(HTML401_ELEMENTS)
    soup = BeautifulSoup(resp, 'html.parser')
    return parse_table(soup.table)


def parse_table(table):
    trs = list(table.find_all('tr'))
    headings = list(map(normalize_heading, trs[0](['th', 'td'])))
    row_class = namedtuple('_table_row_', headings)
    return [
        row_class(*map(get_text, row(['th', 'td'])))
        for row in trs[1:]
        ]


def get_text(elem):
    s = elem.get_text()
    # remove non-ASCII chars
    s = re.sub(r'[^ -~]', ' ', s)
    # normalize white-space
    s = ' '.join(s.split())
    return s


def normalize_heading(elem):
    s = get_text(elem)
    # remove non-alphanumerics chars
    s = re.sub(r'\s', ' ', s)
    s = re.sub(r'[^a-zA-Z_0-9]', '', s)
    s = s.lower()
    return s

#!/bin/python
# -*- coding: utf-8 -*-
"""Scrape HTML 5.1 spec

This is throw-away code to scrape lists of the empty elements, boolean
attributes and composed attributes from the HTML 5.1 draft specification.

You will need to install ``beautifulsoup4`` (and ``webhelpers2``) in order
to run this.  Use at your own risk.

"""
from collections import namedtuple
import re
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen  # py2

from bs4 import BeautifulSoup
from webhelpers2.html import literal


# Index of most recent published HTML 5.1 working draft
HTML51_INDEX = "http://www.w3.org/TR/html51/index.html"

# HTML 4.01 table of elements
HTML401_ELEMENTS = "http://www.w3.org/TR/html401/index/elements.html"


def get_soup(url):
    return BeautifulSoup(urlopen(url), 'html.parser')


def find_table_by_caption(soup, caption):
    match = getattr(caption, 'match',
                    lambda s: s.lower() == caption.lower())

    def matcher(elem):
        if elem.name != 'table':
            return False
        return match(get_text(elem.caption))
    return soup.find(matcher)


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


def parse_table(table):
    rows = iter(table.find_all('tr'))
    headings = [normalize_heading(th) for th in next(rows)(['td', 'th'])]
    row_class = namedtuple('TableRow', headings)
    for row in rows:
        values = tuple(map(get_text, row(['td', 'th'])))
        yield row_class(*values)


def empty_elements(soup):
    table = find_table_by_caption(soup, 'List of elements')
    return set(row.element for row in parse_table(table)
               if row.children == 'empty')


def boolean_attrs(soup):
    table = find_table_by_caption(soup,
                                  re.compile(r'^List of attributes', re.I))
    return set(row.attribute for row in parse_table(table)
               if row.value == 'Boolean attribute')

def compose_attrs(soup):
    table = find_table_by_caption(soup,
                                  re.compile(r'^List of attributes', re.I))
    attrs = {}
    for row in parse_table(table):
        value = row.value.lower()
        if 'space-separated' in value:
            attrs[row.attribute] = literal(" ")
        elif 'comma-separated' in value:
            attrs[row.attribute] = literal(", ")
        elif 'list of integers' in value:
            attrs[row.attribute] = literal(",")
        elif 'media query list' in value:
            attrs[row.attribute] = literal(", ")
        elif 'css declarations' in value:
            attrs[row.attribute] = literal("; ")
    return attrs


def empty_html4_elements(soup):
    table = soup.table
    return set(row.name.lower() for row in parse_table(table)
               if row.empty == 'E')

if __name__ == '__main__':
    from pprint import pprint

    html51_index = get_soup(HTML51_INDEX)
    html401_elements = get_soup(HTML401_ELEMENTS)
    empty_tags = empty_elements(html51_index)
    html4_empty_tags = empty_html4_elements(html401_elements)
    print("HTML 5.1 empty tags")
    pprint(empty_tags)
    print("HTML 4.01 empty tags not included in HTML 5.1")
    pprint(html4_empty_tags - empty_tags)
    print("")

    print("HTML 5.1 boolean attributes")
    pprint(boolean_attrs(html51_index))
    print("")

    print("HTML 5.1 multi-valued attributes")
    pprint(compose_attrs(html51_index))
    print("")

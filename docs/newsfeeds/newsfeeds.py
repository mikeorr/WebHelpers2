from __future__ import absolute_import, print_function, unicode_literals
import copy
import datetime
import os
import sys

from mako.template import Template
from six.moves.urllib import parse

COLLECTION = {
    "title": "My Collection",
    "site_url": "http://example.com/",
    "description": "A bunch of articles.",
    "copyright": "Public domain.",
    "update_date": datetime.date(2014, 8, 12),
    "records": [
        {
            "path": "articles/2",   # Relative to SITE_URL.
            "title": "Article 2",
            "author": "Me",
            "date": datetime.date(2014, 8, 12),
            "update_date": datetime.date(2014, 8, 10),
            "lat": 40.56,
            "lon": -90.23,
            "description": "My article.",
        },
        {
            "path": "articles/1",
            "title": "Article 1",
            "author": "Me",
            "date": datetime.date(2014, 7, 26),
            "update_date": datetime.date(2014, 7, 26),
            "lat": 41.17,
            "lon": -71.51,
            "description": "My earlier article.",
        },
        ]
    }


def make_guid(site, date, path):
    guid_fmt = "tag:{},{}-{}-{}:{}"
    return guid_fmt.format(site, date.year, date.month, date.day, path)


class AtomFeedGenerator(object):
    content_type = b"application/atom+xml"
    date_fmt = "%Y-%m-%dT00:00:00Z" # ISO format except "Z" instead of "UTC".
    output_encoding = "utf-8"
    template = "atom.mako"
    
    def __init__(self, site, site_url, newsfeed_url, debug=False):
        self.site = site
        self.site_url = site_url
        self.newsfeed_url = newsfeed_url
        self.debug = debug

    def render(self, content, output_file, debug=False):
        render = self.get_renderer()
        template_vars = self.get_template_vars(content)
        xml = render(**template_vars)
        f = open(output_file, "w")
        f.write(xml)
        f.close()

    def get_renderer(self):
        kw = {
            "filename": self.template,
            "output_encoding": self.output_encoding,
            }
        if self.debug:
            kw["module_directory"] = os.curdir
        tpl = Template(**kw)
        return tpl.render

    def get_template_vars(self, content):
        update_date = self.get_update_date(content)
        items = self.make_news_items(content)
        ret = {
            "title": content["title"],
            "site_url": self.site_url,
            "newsfeed_url": self.newsfeed_url,
            "update_date": update_date,
            "copyright": content["copyright"],
            "description": content["description"],
            "items": items,
            }
        return ret
        
    def make_news_items(self, content):
        items = []
        for r in content["records"]:
            r = r.copy()
            r["url"] = parse.urljoin(self.site_url, r["path"])
            r["guid"] = make_guid(self.site, r["date"], r["path"])
            r["date"] = r["date"].strftime(self.date_fmt)
            r["update_date"] = r["update_date"].strftime(self.date_fmt)
            items.append(r)
        return items

    def get_update_date(self, content):
        if not content["records"]:
            return None
        return content["records"][0]["date"].strftime(self.date_fmt)


class RSSFeedGenerator(AtomFeedGenerator):
    content_type = b"application/rss+xml"
    date_fmt = "%a, %d %b %Y 00:00:00 -0000"
    template = "rss.mako"


def main():
    debug = "--debug" in sys.argv[1:]
    site = "example.com"
    site_url = "http://example.com/"
    newsfeed_url = site_url + "atom"
    feed = AtomFeedGenerator(site, site_url, newsfeed_url, debug)
    feed.render(COLLECTION, "news.atom")
    newsfeed_url = site_url + "rss"
    feed = RSSFeedGenerator(site, site_url, newsfeed_url, debug)
    feed.render(COLLECTION, "news.rss")

if __name__ == "__main__":  main()

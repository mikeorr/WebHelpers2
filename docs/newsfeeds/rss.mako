<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:georss="http://www.georss.org/georss">
  <channel>
    <title>${title}</title>
    <link>${site_url}</link>
    <description>${description}</description>
    <copyright>${copyright}</copyright>
    <lastBuildDate>${update_date}</lastBuildDate>
% for it in items:
    <item>
      <title>${it['title']}</title>
      <link>${it['url']}</link>
      <description>${it['description']}</description>
      <dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/">${it['author']}</dc:creator>
      <pubDate>${it['date']}</pubDate>
      <guid>${it['guid']}</guid>
% if it['lat'] is not None and it['lon'] is not None:
      <georss:point>${it['lat']} ${it['lon']}</georss:point>
% endif   lat lon
    </item>
% endfor it
  </channel>
</rss>

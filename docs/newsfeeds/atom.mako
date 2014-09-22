<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:georss="http://www.georss.org/georss">
  <title>${title}</title>
  <link href="${site_url}" rel="alternate"></link>
  <link href="${newsfeed_url}" rel="self"></link>
  <id>${newsfeed_url}</id>
  <updated>${update_date}</updated>
  <rights>${copyright}</rights>
% for it in items:
  <entry>
    <title>${it['title']}</title>
    <link href="${it['url']}" rel="alternate"></link>
    <updated>${it['update_date']}</updated>
    <published>${it['date']}</published>
    <author><name>${it['author']}</name></author>
    <id>${it['guid']}</id>
    <summary type="html">${it['description']}</summary>
% if lat is not None and lon is not None:
    <georss:point>${it['lat']} ${it['lon']}</georss:point>
% endif   lat lon
  </entry>
% endfor   incident
</feed>

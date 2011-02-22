import sys
import re
import urllib2
import csv

"""
<a title="RSS Momente si spite "
href="javascript:setUrlHref('http%3A//www.cotidianul.ro/rss/momentesispite.xml')">Momente si spite</a>
"""
if __name__ == "__main__":
    url = 'http://www.cotidianul.ro/rss'
    pattern = r'<a.+?href="(?P<rsslink>.+?\.xml)".*?>(?P<rsstitle>.+?)</a>'
    pattern = re.compile(pattern)

    conn = urllib2.urlopen(url)
    data = conn.read()
    found = pattern.findall(data)
    writer = csv.writer(open('cotidianul.csv', 'w'), delimiter='\t', quotechar='"')
    for link, title in found:
        if not link.startswith('http'):
            link = 'http://www.cotidianul.ro/rss/' + link
        writer.writerow([link, title])

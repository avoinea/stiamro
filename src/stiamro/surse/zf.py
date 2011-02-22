import sys
import re
import urllib2
import csv

if __name__ == "__main__":
    url = 'http://www.zf.ro/rss'
    pattern = r'<a.+?href="(?P<rsslink>/rss.+?)".+?>(?P<rsstitle>[0-9a-zA-Z\s\-\&]+?)</a>'
    pattern = re.compile(pattern)

    conn = urllib2.urlopen(url)
    data = conn.read()
    found = pattern.findall(data)
    writer = csv.writer(open('zf.csv', 'w'), delimiter='\t', quotechar='"')
    for link, title in found:
        if not link.startswith('http'):
            link = 'http://www.zf.ro' + link
        writer.writerow([link, title])

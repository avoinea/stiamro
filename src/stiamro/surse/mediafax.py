import sys
import re
import urllib2
import csv

if __name__ == "__main__":
    url = 'http://www.mediafax.ro/rss-all.html'
    pattern = r'<a.+?href="(?P<rsslink>/.+?\.xml\?\d+)".*?>(?P<rsstitle>.+?)</a>'
    pattern = re.compile(pattern)

    conn = urllib2.urlopen(url)
    data = conn.read()
    found = pattern.findall(data)
    writer = csv.writer(open('mediafax.csv', 'w'), delimiter='\t', quotechar='"')
    for link, title in found:
        if not link.startswith('http'):
            link = 'http://www.mediafax.ro' + link
        writer.writerow([link, title])

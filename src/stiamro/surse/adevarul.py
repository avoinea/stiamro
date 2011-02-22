import sys
import re
import urllib2
import csv

def get(self, url, pattern):
    """
    """

if __name__ == "__main__":
    url = len(sys.argv) > 1 and sys.argv[1] or 'http://www.adevarul.ro/adevarul/rss.html'
    pattern = len(sys.argv) > 2 and sys.argv[2] or r'<a.*href="(?P<rsslink>.+?.rss)".*\>(?P<rsstitle>.+?)</a>'
    pattern = re.compile(pattern)

    conn = urllib2.urlopen(url)
    data = conn.read()
    found = pattern.findall(data)
    writer = csv.writer(open('adevarul.csv', 'w'), delimiter='\t', quotechar='"')
    for link, title in found:
        if not link.startswith('http://'):
            link = 'http://www.adevarul.ro' + link
        writer.writerow([link, title])


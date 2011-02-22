import sys
import re
import urllib2
import csv

if __name__ == "__main__":
    url = 'http://www.9am.ro'
    pattern = r'<a class="rss_icnr".+?href="(?P<rsslink>.+?)".+</a>'
    pattern = re.compile(pattern)

    conn = urllib2.urlopen(url)
    data = conn.read()
    found = pattern.findall(data)
    writer = csv.writer(open('nouaam.csv', 'w'), delimiter='\t', quotechar='"')
    for link in found:
        writer.writerow([link, ])

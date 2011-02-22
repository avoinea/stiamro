import sys
import re
import urllib2
import csv

if __name__ == "__main__":
    url = 'http://www.antena3.ro'
    pattern = r'<link.+?type="application.+?title="(?P<rsstitle>.+?)".+?href="(?P<rsslink>.+?)"'
    pattern = re.compile(pattern)

    conn = urllib2.urlopen(url)
    data = conn.read()
    found = pattern.findall(data)
    writer = csv.writer(open('antena3.csv', 'w'), delimiter='\t', quotechar='"')
    for title, link in found:
        if not link.startswith(url):
            link = url + link
        writer.writerow([link, title])

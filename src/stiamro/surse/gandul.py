import sys
import re
import urllib2
import csv

def get(url, pattern, writter):
    conn = urllib2.urlopen(url)
    data = conn.read()
    found = pattern.findall(data)
    title = url.split('/')[-1]
    for link in found:
        writer.writerow([link, title])

if __name__ == "__main__":
    urls = [
        'http://www.gandul.info/news',
        'http://www.gandul.info/politica',
        'http://www.gandul.info/international',
        'http://www.gandul.info/financiar',
        'http://www.gandul.info/opinii',
        'http://www.gandul.info/reportaj',
        'http://www.gandul.info/sanatate-food-drink',
        'http://www.gandul.info/sport-miscare',
        'http://www.gandul.info/life-style',
        'http://www.gandul.info/media-advertising',
        'http://www.gandul.info/interviurile-gandul',
        'http://www.gandul.info/scoala',
    ]
    pattern = r'<a.*href="(?P<rsslink>.+?.xml\?\d+)".*>'
    pattern = re.compile(pattern)
    writer = csv.writer(open('gandul.csv', 'w'), delimiter='\t', quotechar='"')
    for url in urls:
        get(url, pattern, writer)

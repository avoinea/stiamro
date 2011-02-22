# The file is licenced under Revision 42 of the Beerware Licence.
# <dbatranu@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy <dbatranu@gmail.com> a beer in return.
# David Batranu.


#Requires BeautifulSoup==3.0.8.1

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import urllib2
import re

class Crawler(object):
    """Crawl website, get needed info"""
    def __init__(self, url):
        self.url = url
        self.keywords = []
        self.favicon = None
        self.title = None
        self.description = None
        self.logo = None
        self.other_logos = []
        self.source = None #BeautifulSoup object
        self.feed_links = []
        self.feed_data = None

    def get_favicon(self):
        """Retrieve site favicon.ico"""
        favicon_url = self.clean_link('favicon.ico')
        try:
            urllib2.urlopen(favicon_url)
            self.favicon = favicon_url
        except IOError:
            #favicon unavailable or address incorrect
            pass

    def get_metadata(self):
        """get title, description"""
        self.source = BeautifulSoup(urllib2.urlopen(self.url).read())
        self.title = self.source.html.head.title.string
        metas = self.source.html.findAll('meta', {'name': 'Description'})
        metas.extend(self.source.html.findAll('meta', {'name': 'description'}))
        kw = self.source.html.findAll('meta', {'name': 'Keywords'})
        kw.extend(self.source.html.findAll('meta', {'name': 'keywords'}))
        if metas:
            self.description = metas[0]['content']
        if kw:
            self.keywords = kw[0]['content'].split(',')
    
    def get_feed_links(self):
        """docstring for get_feed_links"""
        possible_feeds = self.source.html.findAll('link', {'rel':'alternate'})
        for feed in possible_feeds:
            if feed.has_key('type') and ('atom' in feed['type'] or \
                'rss' in feed['type']):
                self.feed_links.append(self.clean_link(feed['href']))

    def parse_feed_links(self):
        """docstring for parse_feed_links"""
        mapping = {}
        for feed in self.feed_links:
            try:
                data = urllib2.urlopen(feed)
                data = data.read()
            except:
                mapping[feed] = None
                continue
            feed_source = BeautifulStoneSoup(data)
            try:
                title = feed_source.findAll('title')[0].string
            except IndexError:
                title = ''
            try:
                description = feed_source.findAll('description')[0].string
            except IndexError:
                description = ''
            tags = self.keywords
            if len(title.split(' ')) > 1:
                tags = [x for x in title.split(' ')[1:] if len(x) > 1]
            feed_data = {'title': title,
                         'description': description,
                         'tags': tags,
                         }
            mapping[feed] = feed_data
            
            #try to get logo from feed
            if self.logo:
                continue
            try:
                self.logo = feed_source.findAll('image')[0].url.string
            except:
                pass
        self.feed_data = mapping

    def get_other_logos(self):
        """attempts to get logo other possible logos"""
        self.other_logos.extend([x['src'] for x in 
                                    self.source.findAll('img') 
                                        if 'logo' in x['src']
                                        or 'head' in x['src']])

        #search css files
        
        csss = [self.clean_link(x['href']) for x in 
                    self.source.findAll('link', {'rel' : 'stylesheet'})]
                    
        for css in csss:
            try:
                css_source = urllib2.urlopen(css).read()
            except:
                continue
            search_for = r"url\(['\"]*(.*?logo.*?)['\"]*\)"
            found = re.findall(search_for, css_source)
            self.other_logos.extend([self.clean_link(x) for x in found])

    def clean_link(self, link):
        """docstring for clean_link"""
        if link.startswith('/'):
            return "%s%s" % (self.url, link)
        elif not link.startswith('http://'):
            return "%s/%s" % (self.url, link)
        return link

    def the_works(self):
        """Do everything"""
        self.get_favicon()
        self.get_metadata()
        self.get_feed_links()
        self.parse_feed_links()
        self.get_other_logos()


#site = Crawler('http://cnn.com')
#site = Crawler('http://adevarul.ro')
#site = Crawler('http://hotnews.ro')
#site = Crawler('http://www.realitatea.net')
#site = Crawler('http://www.dumisblog.com')
site = Crawler('http://www.gds.ro')
site.the_works()
from pprint import pprint
pprint([(x, y) for (x, y) in site.__dict__.items() if x != 'source'])

import re
from difflib import SequenceMatcher
from zope.app import zapi
import feedparser
from urllib2 import urlopen

from zope.component import getMultiAdapter
from zope.formlib.form import Fields, PageAddForm, PageEditForm, applyChanges
from zope.app.container.interfaces import INameChooser
from zope.publisher.browser import BrowserPage
from zope.app.file.interfaces import IImage

from stiamro.content.interfaces import IServer
from stiamro.content.server import Server

from z3c.indexer.search import SearchQuery
from z3c.indexer.query import Eq

from allen.utils.cache import servercache

class ServerAddPage(PageAddForm):
    form_fields = Fields(IServer)

    def _get_id(self, url):
        """ Get id from url
        """
        name = url.split('.')[-2:]
        return '.'.join(name)

    def _discover(self, url):
        """ Discover server properties
        """
        if url.endswith('/'):
            url = url[:-1]
        data = urlopen(url)
        html = data.read()
        pattern = re.compile(r'application/rss\+xml.*href=\"(?P<rsslink>.*)\"')
        found = pattern.search(html)
        if not found:
            pattern = re.compile(r'href=\"(?P<rsslink>.*)\".*application/rss\+xml')
            found = pattern.search(html)
        if not found:
            return {}

        rss = found.group('rsslink')
        if not rss.startswith('http'):
            if rss.startswith('/'):
                rss = url + rss
            else:
                rss = url + '/' + rss

        server = feedparser.parse(rss)
        title = server.feed.get('title', '')
        description = server.feed.get('subtitle', '')

        return {
            'title': title,
            'description': description,
            'url': url,
        }

    def create(self, data):
        ob = Server()
        url = data.get('url')
        data = self._discover(url)

        domain = self._get_id(url)
        uid = INameChooser(self.context).chooseName(domain, ob)
        setattr(ob, '_tmp_id', uid)
        applyChanges(ob, self.form_fields, data)
        return ob

    def add(self, obj):
        name = getattr(obj, '_tmp_id', 'server')
        delattr(obj, '_tmp_id')
        self.context[name] = obj
        self._finished_add = True
        return obj

    def nextURL(self):
        return "."

class ServerEditPage(PageEditForm):
    form_fields = Fields(IServer)

class ServerContent(BrowserPage):
    """ Content
    """
    @property
    def items(self):
        source = self.context.__name__
        source_criteria = Eq('stiam.ro.source', source)
        query = SearchQuery(source_criteria)
        brains = query.searchResults(sort_index='stiam.ro.effective',
                                     reverse=True, limit=30)

        duplicate = ""
        index = 0
        for brain in brains:
            if index >= 15:
                raise StopIteration

            title = getattr(brain, "title", "")
            s = SequenceMatcher(lambda x: x == "", title, duplicate)
            if s.ratio() > 0.6:
                continue

            duplicate = title
            index += 1
            yield brain

    @property
    def etag(self):
        etag = getMultiAdapter((self.context, self.request), name=u'index.etag')
        return etag()

    def thumbnail(self, context=None, size='icon', **kwargs):
        if not context:
            context = self.context

        for key, doc in context.items():
            if key == 'icon.png':
                continue
            if not IImage.providedBy(doc):
                continue

            scale = getMultiAdapter((doc, self.request), name=u'scale')
            try:
                thumb = scale.publishTraverse(self.request, size)
            except Exception, err:
                thumb = ''
            if thumb and thumb.getSize():
                return zapi.absoluteURL(doc, self.request)
        return ''

    @servercache
    def __call__(self, **kwargs):
        return self.index()

class ServerView(ServerContent):
    """ View
    """
    def __call__(self, **kwargs):
        return self.index()

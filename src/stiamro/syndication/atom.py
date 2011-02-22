from zope import datetime as zope_datetime
from base64 import encodestring
import urlparse
import urllib
from datetime import datetime
from zope.traversing.browser import absoluteURL
from zope.publisher.browser import BrowserPage
from zope.component import getMultiAdapter
from allen.utils.cache import servercache
from stiamro.utils.interfaces import ILastUpdated

from stiamro import bucharest, utc

class Atom(BrowserPage):
    """ Atom feed
    """
    @property
    def uid(self):
        """
        http://diveintomark.org/archives/2004/05/28/howto-atom-id - article
        about constructing id
        """
        scheme, netloc, path, query, fragment = urlparse.urlsplit(self.permalink)
        location, port = urllib.splitport(netloc)
        uid = "tag:%s,%s:%s" % (location, self.updated.strftime('%Y-%m-%d'), path)
        return uid

    @property
    def title(self):
        return 'stiam.ro - ' + self.context.title

    @property
    def subtitle(self):
        return self.context.description

    @property
    def updated(self):
        res = ILastUpdated(self.context)()
        if not isinstance(res, datetime):
            res = datetime(2009, 01, 01, 0, 0, 0, 0, utc)
        return res

    @property
    def updated_str(self):
        return self.updated.strftime('%Y-%m-%dT%H:%M:%S+02:00')

    @property
    def updated_rfc(self):
        lmt = zope_datetime.time(self.updated.isoformat())
        return zope_datetime.rfc1123_date(lmt)

    @property
    def permalink(self):
        return absoluteURL(self.context, self.request)

    @property
    def atomlink(self):
        return self.permalink + '/atom.xml'

    @property
    def icon(self):
        return '/@@/www/favicon.png'


    @property
    def logo(self):
        return '/@@/www/logo.png'

    @property
    def etag(self):
        res = getMultiAdapter((self.context, self.request), name=u'index.etag')
        res = res(atom=1)
        res = res.split('\n')[0]
        return res

    @property
    def items(self):
        index = getMultiAdapter((self.context, self.request), name=u'index.html')
        for item in index.items:
            yield item

    @servercache
    def render(self):
        return self.index()

    def __call__(self, **kwargs):
        self.request.response.setHeader('content-type', 'text/xml;charset=utf-8')

        # Check for etag
        etag = self.request.getHeader('If-None-Match', None)
        if etag and etag == self.etag:
            self.request.response.setStatus(304)
            return ''

        # Check for modified
        last_modified = self.request.getHeader('If-Modified-Since', None)
        if last_modified and last_modified == self.updated_rfc:
            self.request.response.setStatus(304)
            return ''

        self.request.response.setHeader('Last-Modified', self.updated_rfc)
        self.request.response.setHeader('etag', self.etag)
        return self.render()

class AtomEntry(BrowserPage):
    """ Atom entry
    """
    def __init__(self, context, request):
        super(AtomEntry, self).__init__(context, request)
        self.page = ''

    @property
    def uid(self):
        """
        http://diveintomark.org/archives/2004/05/28/howto-atom-id - article
        about constructing id
        """
        scheme, netloc, path, query, fragment = urlparse.urlsplit(self.permalink)
        location, port = urllib.splitport(netloc)
        uid = "tag:%s,%s:%s" % (location, self.updated.strftime('%Y-%m-%d'), path)
        return uid

    @property
    def title(self):
        return self.context.title

    @property
    def subtitle(self):
        return self.context.description

    @property
    def thumbnail(self):
        index = getMultiAdapter((self.context, self.request), name=u'index.html')
        thumb = index.thumbnail()
        if thumb:
            return thumb + '/scale/thumbnail'
        return ''

    @property
    def permalink(self):
        return absoluteURL(self.context, self.request)

    @property
    def updated(self):
        return self.context.updated or datetime.now(bucharest)

    @property
    def updated_str(self):
        return self.updated.strftime('%Y-%m-%dT%H:%M:%S+02:00')

    @property
    def author(self):
        server = self.context.__parent__.__parent__
        return server.url

    def __call__(self, **kwargs):
        self.page = kwargs.get('page', '')
        return self.index()

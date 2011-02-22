import logging
from difflib import SequenceMatcher
from base64 import encodestring
from datetime import datetime
from zope.component import getMultiAdapter, getUtility
from zope.formlib.form import Fields, PageAddForm, PageEditForm, applyChanges
from zope.app.container.interfaces import INameChooser
from zope.publisher.browser import BrowserPage

from stiamro import bucharest
from stiamro.content.interfaces import ISite
from stiamro.content.interfaces import IPage
from stiamro.content.page import Page
from allen.utils.cache import servercache
from stiamro.utils.interfaces import ILastUpdated

from z3c.indexer.search import SearchQuery
from z3c.indexer.query import AnyOf

from allen.catalog.timeline.interfaces import ITimeline

logger = logging.getLogger('stiamro.page')

class PageAddPage(PageAddForm):
    """ Add a Page
    """
    form_fields = Fields(IPage)
    def create(self, data):
        ob = Page()

        title = data.get('title', 'stire')
        uid = INameChooser(self.context).chooseName(title, ob)
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
        return "../@@edit.html"


class PageEditPage(PageEditForm):
    form_fields = Fields(IPage)


class PageContent(BrowserPage):
    """ Content
    """
    @property
    def items(self):
        tags = self.context.tags or [self.context.__name__]
        max_items = self.context.max_items * 2

        anyOfQuery = AnyOf('stiam.ro.tags', tags)
        query = SearchQuery(anyOfQuery)
        brains = query.searchResults(sort_index='stiam.ro.effective',
                                     reverse=True, limit=max_items)

        index = 0
        duplicate = ""
        for brain in brains:
            if index >= max_items / 2:
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

    @servercache
    def __call__(self, **kwargs):
        return self.index()

class PageSitemap(PageContent):
    """ Google sitemap
    """
    def lastmodified(self, page):
        date = getattr(page, 'updated', None)
        if not isinstance(date, datetime):
            return ''
        return date.isoformat()

    @property
    def items(self):
        tags = self.context.tags or [self.context.__name__]
        now = datetime.now(bucharest)
        max_items = 500

        logger.info('Query %s start %s', tags, now.strftime('%H:%M:%S'))

        anyOfQuery = AnyOf('stiam.ro.tags', tags)
        query = SearchQuery(anyOfQuery)
        brains = query.searchResults(sort_index='stiam.ro.effective',
                                     reverse=True, limit=max_items)

        logger.info('Query %s end %s', tags, datetime.now(bucharest).strftime('%H:%M:%S'))

        for brain in brains:
            yield brain

    @property
    def etag(self):
        etag = getMultiAdapter((self.context, self.request), name=u'index.etag')
        return etag(page='sitemap.xml')

    @servercache
    def __call__(self, **kwargs):
        return self.index()

class PageView(PageContent):
    """ View
    """
    def __call__(self, **kwargs):
        return self.index()

class PageEtag(BrowserPage):
    """ Get etag
    """
    def __call__(self, **kwargs):
        modified = ILastUpdated(self.context)()
        etag = self.context.__name__
        if isinstance(modified, datetime):
            etag += modified.isoformat().split('.')[0]
        if kwargs:
            etag += '%s' % kwargs
        return encodestring(etag)

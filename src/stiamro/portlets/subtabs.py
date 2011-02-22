from zope.component import queryAdapter
from zope.publisher.browser import BrowserPage
from zope.traversing.browser.absoluteurl import absoluteURL
from stiamro.content.interfaces import (
    ISite,
    ISortedContent,
    IPage,
    IServer,
    INews
)
from allen.content.section.interfaces import ISection

class Subtabs(BrowserPage):
    """ Breadcrumbs
    """
    @property
    def _site_items(self):
        content = queryAdapter(self.context, ISortedContent)
        if not content:
            raise StopIteration

        for page in content.children(IPage, sort_by='order', reverse=False):
            yield page

    @property
    def _page_items(self):
        content = queryAdapter(self.context.__parent__, ISortedContent)
        if not content:
            raise StopIteration

        for page in content.children(IPage, sort_by='order', reverse=False):
            if page == self.context:
                continue
            yield page

    @property
    def _server_items(self):
        content = queryAdapter(self.context, ISortedContent)
        if not content:
            raise StopIteration

        for page in content.children(INews, sort_by='title', reverse=False):
            yield page

    @property
    def _news_items(self):
        content = queryAdapter(self.context.__parent__, ISortedContent)
        if not content:
            raise StopIteration

        for page in content.children(INews, sort_by='title', reverse=False):
            if page == self.context:
                continue
            yield page

    @property
    def items(self):
        items = []

        if ISite.providedBy(self.context):
            return self._site_items
        elif IPage.providedBy(self.context):
            return self._page_items
        elif IServer.providedBy(self.context):
            return self._server_items
        elif INews.providedBy(self.context):
            return self._news_items
        return []

    def __call__(self, **kwargs):
        return self.index()

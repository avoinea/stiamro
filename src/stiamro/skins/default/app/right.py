import operator
from zope.component import ComponentLookupError
from zope.component import getMultiAdapter
from zope.component import queryAdapter
from zope.app.component.hooks import getSite
from stiamro.content.interfaces import IPage, ISortedContent, IServer, INews, ISite
from zope.viewlet.viewlet import ViewletBase

class RightViewlet(ViewletBase):
    """ View
    """
    def __init__(self, context, request, view, manager):
        super(RightViewlet, self).__init__(context, request, view, manager)
        self.page = self.context
        self.context = getSite()

    @property
    def tabs(self):
        """ Return the first IPage subobject
        """
        if ISite.providedBy(self.page):
            yield self.page['sursa']
            raise StopIteration

        content = queryAdapter(self.context, ISortedContent)
        if not content:
            raise StopIteration

        for page in content.children(IPage, sort_by='order', reverse=False):
            if page == self.page:
                continue
            yield page

    def portlet(self, page):
        html = getMultiAdapter((page, self.request), name=u'content.portlet')
        return html()

class NewsRightViewlet(ViewletBase):
    """ Right side for News
    """
    def __init__(self, context, request, view, manager):
        super(NewsRightViewlet, self).__init__(context, request, view, manager)
        self.page = self.context

        if INews.providedBy(self.context):
            self.context = context.__parent__

    @property
    def tabs(self):
        """ Return the first IPage subobject
        """
        content = queryAdapter(self.context, ISortedContent)
        if not content:
            raise StopIteration

        for page in content.children(INews, sort_by='title', reverse=False):
            if page == self.page:
                continue
            yield page

    def portlet(self, page):
        html = getMultiAdapter((page, self.request), name=u'content.portlet')
        return html()

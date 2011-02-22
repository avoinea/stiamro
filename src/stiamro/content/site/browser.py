import logging
from zope.component import getUtility
from datetime import datetime
from zope.component import getMultiAdapter, queryAdapter
from zope.publisher.browser import BrowserPage
from stiamro.content.interfaces import IPage, ISortedContent
from stiamro.utils.interfaces import ILastUpdated
from stiamro.google.insights.interfaces import IInsights
from allen.utils.cache import servercache

logger = logging.getLogger('SITE')

class SiteView(BrowserPage):
    """ View
    """
    @servercache
    def insights(self):
        try:
            content = getUtility(IInsights)
        except Exception, err:
            logger.exception(err)
            return ''

        view = getMultiAdapter((content, self.request), name=u'content.html')
        if not view:
            return ''

        return view()

    @property
    def tabs(self):
        """ Return the first IPage subobject
        """
        content = queryAdapter(self.context, ISortedContent)
        if not content:
            raise StopIteration

        for page in content.children(IPage, sort_by='order', reverse=False):
            yield page

    def portlet(self, page):
        html = getMultiAdapter((page, self.request), name=u'content.portlet')
        return html()

    @property
    def etag(self):
        etag = getMultiAdapter((self.context, self.request), name=u'index.etag')
        etag = etag(root=1)
        return etag

    def lastmodified(self, page):
        date = ILastUpdated(page)()
        if not isinstance(date, datetime):
            return ''
        date = date.isoformat()
        # tz info
        if '+' not in date:
            date = date + '+00:00'
        return date

    def __call__(self, **kwargs):
        return self.index()

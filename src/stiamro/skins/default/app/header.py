from datetime import datetime, timedelta
from zope.component import queryAdapter
from stiamro.content.interfaces import IPage, ISortedContent
from zope.viewlet.viewlet import ViewletBase
from zope.traversing.browser import absoluteURL
from stiamro import bucharest
class HeaderViewlet(ViewletBase):
    """ Header
    """
    def __init__(self, context, request, view, manager):
        super(HeaderViewlet, self).__init__(context, request, view, manager)
        if not IPage.providedBy(self.context):
            self.context = self.homepage

    def title(self):
        return getattr(self.context, 'title', '')

    def url(self):
        return absoluteURL(self.context, self.request)

    @property
    def now(self):
        now = datetime.now(bucharest)
        return now.strftime('%Y/%m/%d %H:%M:%S')

    @property
    def homepage(self):
        """ Return the first IPage subobject
        """
        content = queryAdapter(self.context, ISortedContent)
        if not content:
            return None

        for page in content.children(IPage, sort_by='order', reverse=False):
            return page
        return None

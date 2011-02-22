from datetime import datetime
from zope.component import queryAdapter, queryUtility
from stiamro.content.interfaces import IPage, ISortedContent
from zope.viewlet.viewlet import ViewletBase
from zope.traversing.browser import absoluteURL
from zope.app.applicationcontrol.applicationcontrol import applicationController
from stiamro.utils.interfaces import IText
from stiamro.content.interfaces import ISite

class HeadViewlet(ViewletBase):
    """ View
    """
    def __init__(self, context, request, view, manager):
        super(HeadViewlet, self).__init__(context, request, view, manager)
        self.page = self.context
        while IPage.providedBy(self.context):
            self.context = self.context.__parent__

    @property
    def started(self):
        stamp = applicationController.getStartTime()
        try:
            stamp = datetime.fromtimestamp(stamp)
        except (ValueError, TypeError), err:
            return stamp
        else:
            return stamp.strftime('%d%m%Y%H%M')

    @property
    def headtitle(self):
        if ISite.providedBy(self.page):
            return u'Ziare online, ziarul tau, stiri online de ultima ora, jocuri'

        title = getattr(self.page, 'title', '')
        if not title:
            return u'Revista presei romanesti'

        util = queryUtility(IText)
        title = util.translate(title)
        return util.truncate(title)

    @property
    def headsubtitle(self):
        if ISite.providedBy(self.page):
            return (u'stiam.ro - ziare online, ziarul si revista presei '
                    'romanesti - contine stiri online de ultima ora, jocuri '
                    'ca solitaire, sudoku, bomberman, dartz, domino, golf '
                    'si altele')

        description = getattr(self.page, 'description', u'')
        if not description:
            return (u'Revista presei romanesti contine stiri de pe cele mai '
                    'importante site-uri de stiri romanesti. Jocuri: '
                    'solitaire, sudoku si altele')

        util = queryUtility(IText)
        description = util.translate(description)
        return util.truncate(description, words=27, length=135)

    @property
    def headkeywords(self):
        util = queryUtility(IText)
        return ', '.join(util.keywords(self.headtitle, self.headsubtitle))

    @property
    def headurl(self):
        return absoluteURL(self.page, self.request)

    def title(self, page):
        return getattr(page, 'title', '')

    def url(self, page):
        return absoluteURL(page, self.request)

    @property
    def pages(self):
        """ Return the first IPage subobject
        """
        content = queryAdapter(self.context, ISortedContent)
        if not content:
            raise StopIteration

        for page in content.children(IPage, sort_by='order', reverse=False):
            yield page

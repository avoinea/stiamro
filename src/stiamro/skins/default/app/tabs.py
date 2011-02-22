""" Tabs
"""
from zope.viewlet.viewlet import ViewletBase
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite
from stiamro.content.interfaces import ISortedContent
from stiamro.content.interfaces import ISite, INews

from allen.content.section.interfaces import ISection

class TabsViewlet(ViewletBase):
    """ View
    """
    def __init__(self, context, request, view, manager):
        super(TabsViewlet, self).__init__(context, request, view, manager)
        self.page = context
        self.context = getSite()

    @property
    def tabs(self):
        """ Return the first IPage subobject
        """
        root = ISite.providedBy(self.page)
        yield {
            'url': absoluteURL(self.context, self.request),
            'title': 'Revista presei',
            'current': root
        }

        if INews.providedBy(self.page):
            server = self.page.__parent__
            title = getattr(server, 'title', server.__name__)
            if len(title) > 25:
                title = title[:25] + '...'
            yield {
                'url': absoluteURL(server, self.request),
                'title': title,
                'current': False
            }

        if not (root or ISection.providedBy(self.page)):
            title = getattr(self.page, 'title', self.page.__name__)
            if len(title) > 25:
                title = title[:25] + '...'

            yield {
                'url': absoluteURL(self.page, self.request),
                'title': title,
                'current': True
            }

        content = ISortedContent(self.context)
        for section in content.children(ISection, sort_by='order'):
            yield {
                'url': absoluteURL(section, self.request),
                'title': section.title,
                'current': self.page.__name__ == section.__name__
            }

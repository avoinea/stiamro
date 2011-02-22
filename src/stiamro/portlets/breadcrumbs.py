from zope.publisher.browser import BrowserPage
from zope.traversing.browser.absoluteurl import absoluteURL
from stiamro.content.interfaces import ISite

from allen.content.section.interfaces import ISection

class Breadcrumbs(BrowserPage):
    """ Breadcrumbs
    """
    @property
    def items(self):
        items = []

        page = self.context
        while 1:
            items.insert(0, {
                'url': absoluteURL(page, self.request),
                'title': page.title or page.__name__
            })
            if ISection.providedBy(page):
                break

            if ISite.providedBy(page):
                break

            page = page.__parent__

        for page in items:
            yield page

    def __call__(self, **kwargs):
        return self.index()

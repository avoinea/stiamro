from zope.component import queryAdapter
from zope.publisher.browser import BrowserPage
from stiamro.content.interfaces import ISortedContent, IPage

class FeedsView(BrowserPage):
    """ All feeds view
    """
    def __call__(self, **kwargs):
        return self.index()

    @property
    def pages(self):
        """ Return the IPage subobject
        """
        content = queryAdapter(self.context, ISortedContent)
        if not content:
            raise StopIteration

        for page in content.children(IPage, sort_by='order', reverse=False):
            yield page

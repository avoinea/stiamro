""" Portlet for content
"""
from zope.component import getMultiAdapter
from zope.publisher.browser import BrowserPage
from allen.utils.cache import servercache
from zope.traversing.browser import absoluteURL

class ContentPortlet(BrowserPage):
    """ Display content as a 5 items portlet.
    """
    def news(self, max_items=5):
        """ Return news items
        """
        view = getMultiAdapter((self.context, self.request), name=u'index.html')
        index = 0
        for newsitem in view.items:
            index += 1
            if index > max_items:
                raise StopIteration
            yield newsitem

    def thumbnail(self, newsitem):
        """ Return icon
        """
        index = getMultiAdapter((newsitem, self.request), name=u'index.html')
        thumb = getattr(index, 'thumbnail', None)
        thumb = thumb and thumb(from_parent=True)
        if thumb:
            return thumb
        return ''

    @property
    def etag(self):
        """ Used by servercache decorator
        """
        etag = getMultiAdapter((self.context, self.request), name=u'index.etag')
        etag = etag(content_portlet=absoluteURL(self.context, self.request))
        return etag

    def relative_id(self, newsitem):
        view = getMultiAdapter((newsitem, self.request), name=u'index.html')
        return getattr(view, 'relative_id', '')

    @servercache
    def __call__(self, **kwargs):
        return self.index()

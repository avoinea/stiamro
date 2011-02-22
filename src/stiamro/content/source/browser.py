from zope.app import zapi
from zope.component import queryAdapter, getMultiAdapter
from zope.publisher.browser import BrowserPage
from stiamro.content.interfaces import IServer, ISortedContent
from allen.utils.cache import servercache
from zope.app.file.interfaces import IImage

class Content(BrowserPage):
    """ Content
    """
    @property
    def items(self):
        content = queryAdapter(self.context, ISortedContent)
        if not content:
            raise StopIteration

        for child in content.children(IServer, sort_by='title', reverse=False):
            yield child

    @property
    def etag(self):
        etag = getMultiAdapter((self.context, self.request), name=u'index.etag')
        return etag()

    def thumbnail(self, context=None, size='album', **kwargs):
        if not context:
            context = self.context

        for key, doc in context.items():
            if key == 'icon.png':
                continue
            if not IImage.providedBy(doc):
                continue

            scale = getMultiAdapter((doc, self.request), name=u'scale')
            try:
                thumb = scale.publishTraverse(self.request, size)
            except Exception, err:
                thumb = ''
            if thumb and thumb.getSize():
                return zapi.absoluteURL(doc, self.request)
        return ''

    @servercache
    def __call__(self, **kwargs):
        return self.index()


class View(Content):
    """ View
    """
    def __call__(self, **kwargs):
        return self.index()

from zope.component import getMultiAdapter
from allen.utils.cache import servercache
from content import ContentPortlet

class MobilePortlet(ContentPortlet):
    @property
    def etag(self):
        """ Used by servercache decorator
        """
        etag = getMultiAdapter((self.context, self.request), name=u'index.etag')
        etag = etag(mobile_portlet=1)
        return etag

    @servercache
    def __call__(self, **kwargs):
        return self.index()

from zope.interface import implements
from stiamro.google.api import Connection
from interfaces import IGoogleAnalyticsConnection

class GoogleAnalyticsConnection(object):
    """ Access Google Analytics
    """
    implements(IGoogleAnalyticsConnection)

    def __call__(self, token):
        self.connection = Connection(token)
        return self.connection

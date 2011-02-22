from datetime import datetime
from zope.interface import implements
from interfaces import ILastUpdated

from stiamro import bucharest

class LastUpdated(object):
    """ See interface
    """
    implements(ILastUpdated)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        """ See interface
        """
        now = datetime.now(bucharest)
        return datetime(now.year, now.month, now.day, now.hour)

import datetime
from zope.interface import implements
from zope.app.folder import Folder

from interfaces import IAnalytics
from interfaces import IAnalyticsReport
from zope.dublincore.property import DCProperty

from stiamro import bucharest

class Analytics(Folder):
    """ Google Analytics connection
    """
    implements(IAnalytics)

    title = DCProperty('title')
    description = DCProperty('description')
    _token = ''

    @property
    def token(self):
        return self._token

class AnalyticsReport(Folder):
    """ Google Analytics report
    """
    implements(IAnalyticsReport)

    title = DCProperty('title')
    description = DCProperty('description')

    table = 'ga:22589601'
    dimensions = ('ga:pagePath',)
    metrics = ('ga:pageviews',)
    filters = 'ga:pagePath=@/sursa/'
    sort = '-ga:pageviews'
    start_index = 1
    max_results = 100

    def __init__(self, **kwargs):
        super(AnalyticsReport, self).__init__()

    @property
    def start_date(self):
        past = datetime.datetime.now(bucharest) - datetime.timedelta(1)
        return datetime.date(past.year, past.month, past.day)

    @property
    def end_date(self):
        future = datetime.datetime.now(bucharest) + datetime.timedelta(1)
        return datetime.date(future.year, future.month, future.day)

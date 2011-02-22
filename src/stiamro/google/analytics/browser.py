""" Analytics browser pages
"""
import operator
import logging

from zope.component import getUtility, queryUtility
from content import AnalyticsReport
from interfaces import IAnalytics, IGoogleAnalyticsConnection, IAnalyticsReport, IXMLParser
from zope.publisher.browser import BrowserPage

logger = logging.getLogger('stiamro.google')
#
# Register service
#
class AnalyticsRegisterPage(BrowserPage):
    """ Register token
    """
    def _redirect(self, msg=""):
        return msg

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)

        token = kwargs.get('token', '') or ''
        utility = getUtility(IGoogleAnalyticsConnection)

        # Reset tooken
        if not token:
            conn = utility(self.context.token)
            response = conn.request(scope='/accounts/AuthSubRevokeToken')
            self.context._token = token
            if response:
                return self._redirect('Token unregistered successfully')
            else:
                return self._redirect('Token removed, but you have to manually unregister it at '
                                      'https://www.google.com/accounts/IssuedAuthSubTokens')

        # Update token
        conn = utility(token)

        # Replace single call token with a session one
        token = conn.token2session()
        if not token:
            return self._redirect(("An error occured during registration process. "
                                   "Please check the log file"))
        self.context._token = token
        return self._redirect('Successfully registered with Google.')

class AnalyticsViewPage(BrowserPage):
    """ View Google Analytics connection information
    """
    @property
    def status_error(self):
        if not self.context.token:
            return {
                'status': 404,
                'error': 'Not initialized'
            }
        utility = getUtility(IGoogleAnalyticsConnection)
        conn = utility(self.context.token)
        status, error = conn.status
        return {
            'status': status,
            'error': error
        }

    def __call__(self, **kwargs):
        return self.index()

class ReportViewPage(BrowserPage):
    """ Index xml
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        util = queryUtility(IAnalytics)
        self.token = util and util.token or ''

    def error_xml(self, query):
        res = ['<?xml version="1.0" ?>']
        res.append('<error>')
        res.append('<query><![CDATA[%s]]></query>' % query)
        res.append('</error>')
        return '\n'.join(res)

    def xml(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)
        scope = '/analytics/feeds/data'
        dimensions = ','.join(self.context.dimensions)
        metrics = ','.join(self.context.metrics)
        query = {
            'ids': self.context.table,
            'dimensions': dimensions,
            'metrics': metrics,
            'filters': self.context.filters,
            'sort': self.context.sort,
            'start-date': str(self.context.start_date),
            'end-date': str(self.context.end_date),
            'start-index': self.context.start_index,
            'max-results': self.context.max_results,
        }
        # Filter None parameters
        query = dict((key, value) for key, value in query.items() if value)

        utility = getUtility(IGoogleAnalyticsConnection)
        conn = utility(self.token)
        response = conn.request(scope=scope, data=query, method='GET')

        content_type = kwargs.get('content_type', 'text/xml')
        if self.request and content_type:
            self.request.response.setHeader('content-type', content_type)
        if not response:
            return self.error_xml(query)
        return response.read()

    def table(self, **kwargs):
        """ Return a table generator
        """
        parser = getUtility(IXMLParser)
        return parser(self.xml(content_type=None))

    def brains(self):
        brains = {}
        for dimenstions, metrics in self.table():
            path = dimenstions.get('ga:pagePath', '')
            views = metrics.get('ga:pageviews', 0)
            if not (path or views):
                continue

            if path.startswith('/ajax'):
                path = path.replace('/ajax', '', 1)
            elif path.startswith('/exit'):
                path = path.replace('/exit', '', 1)
            brains.setdefault(path, 0)
            brains[path] += int(views)
        items = brains.items()
        items.sort(key=operator.itemgetter(1), reverse=True)

        for path, count in items:
            yield path, count

    def __call__(self, **kwargs):
        for brain, count in self.brains():
            print brain, count
        return 'Done'

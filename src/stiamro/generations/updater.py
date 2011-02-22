""" Evolution 2
"""
import logging
from stiamro.content.interfaces import INews, IServer
from stiamro.manage.updater import NewsUpdater
from zope.publisher.browser import BrowserPage
from zope.traversing.browser import absoluteURL

logger = logging.getLogger('stiamro.generation.2')

class Update(BrowserPage):
    """ Update updaters
    """
    def __call__(self, **kwargs):
        sursa = self.context['sursa']
        for server in sursa.values():
            if not IServer.providedBy(server):
                continue
            for news in server.values():
                if not INews.providedBy(news):
                    continue
                if 'updater' in news:
                    del news['updater']

                logger.info('Update updater for %s' % (
                    absoluteURL(news, self.request)))
                updater = NewsUpdater()
                news['updater'] = updater

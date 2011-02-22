import logging
import transaction
from datetime import datetime, timedelta
from zope.component import queryUtility, queryMultiAdapter
from zope.intid.interfaces import IIntIds
from stiamro.content.interfaces import INewsItem, INews, IServer
from zope.traversing.browser import absoluteURL

from zope.publisher.browser import BrowserPage
from z3c.indexer.indexer import index as z3c_index

from allen.catalog.timeline.interfaces import ITimeline
from stiamro import utc

logger = logging.getLogger('stiamro.reindex.1')

class ReindexNews(BrowserPage):
    def __call__(self, **kwargs):
        """ Evolve
        """
        start = datetime.now()
        intids = queryUtility(IIntIds)
        timeline = queryUtility(ITimeline, name=u'news.timeline')

        logger.info('Indexing objects: %s', start.strftime('%Y-%m-%d %H:%M:%S'))
        tags = [self.context.__name__]
        for newsitem in self.context.values():
            if not INewsItem.providedBy(newsitem):
                continue

            logger.info('Index object %s', absoluteURL(newsitem, self.request))

            if not newsitem.tags:
                logger.info('Fix tags')
                newsitem.tags = tags

            if not newsitem.updated.tzinfo:
                args = newsitem.updated.timetuple()[:6] + (0, utc)
                logger.info('Fix updated datetime')
                newsitem.updated = datetime(*args)

            intids.register(newsitem)
            z3c_index(newsitem)
            timeline.index(newsitem)

        logger.info('Commit transaction')
        end = datetime.now()

        delta = end - start
        logger.info('Done: %s', end.strftime('%Y-%m-%d %H:%M:%S'))
        logger.info('Done in %s seconds', delta.seconds)
        return 'Done in %s seconds' % delta.seconds

class ReindexServer(BrowserPage):
    def __call__(self, **kwargs):
        """ Evolve
        """
        start = datetime.now()

        logger.info('Indexing objects: %s', start.strftime('%Y-%m-%d %H:%M:%S'))
        for news in self.context.values():
            if not INews.providedBy(news):
                continue

            reindex = queryMultiAdapter((news, self.request), name=u'reindex.html')
            reindex()

            logger.info('Commit transaction')
            transaction.commit()

        end = datetime.now()

        delta = end - start
        logger.info('Done: %s', end.strftime('%Y-%m-%d %H:%M:%S'))
        logger.info('Done in %s seconds', delta.seconds)
        return 'Done in %s seconds' % delta.seconds

class ReindexSource(BrowserPage):
    def __call__(self, **kwargs):
        """ Evolve
        """
        start = datetime.now()
        logger.info('Indexing objects: %s', start.strftime('%Y-%m-%d %H:%M:%S'))

        for server in self.context.values():
            if not IServer.providedBy(server):
                continue
            reindex = queryMultiAdapter((server, self.request), name=u'reindex.html')
            reindex()

            logger.info('Commit transaction')
            transaction.commit()

        end = datetime.now()

        delta = end - start
        logger.info('Done: %s', end.strftime('%Y-%m-%d %H:%M:%S'))
        logger.info('Done in %s seconds', delta.seconds)
        return 'Done in %s seconds' % delta.seconds

from zope.component import getUtility
from z3c.indexer.search import SearchQuery
from z3c.indexer.query import Le
from stiamro import bucharest
from z3c.indexer import interfaces

class ReindexBySourcesIndex(BrowserPage):
    def __call__(self, **kwargs):
        """ Evolve
        """
        start = datetime.now(bucharest)
        logger.info('Reindex stiam.ro.source started: %s',
                    start.strftime('%Y-%m-%d %H:%M:%S'))

        end = datetime.now(bucharest) + timedelta(3)
        leQuery = Le('stiam.ro.effective', end)
        query = SearchQuery(leQuery)
        brains = query.searchResults()
        logger.info('Reindex %s newsitems', len(brains))

        intids = getUtility(IIntIds)
        sourceIndex = getUtility(interfaces.IIndex, 'stiam.ro.source')

        for index, brain in enumerate(brains):
            server = brain.__parent__.__parent__.__name__
            oid = intids.getId(brain)
            sourceIndex.doIndex(oid, server)

            if index % 500 == 0:
                logger.info('Indexed %s items', index)

        logger.info('Reindex stiam.ro.source done: %s',
                    datetime.now(bucharest) - start)

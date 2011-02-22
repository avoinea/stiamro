import logging
import transaction
from datetime import datetime, timedelta
from zope.component import queryUtility
from zope.publisher.browser import BrowserPage
from zope.intid.interfaces import IIntIds
from zope.traversing.browser import absoluteURL

from z3c.indexer.query import Le
from z3c.indexer.search import SearchQuery

from stiamro import bucharest, utc
logger = logging.getLogger('NEWS CLEANUP')

class Cleanup(BrowserPage):
    """ Remove all news items
    """
    def _cleanup(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)
        maxdays = kwargs.get('days', 7)
        try:
            maxdays = int(maxdays)
        except Exception, err:
            maxdays = 7

        now = datetime.now(bucharest)

        # Prevent full cleanup
        maxdays = timedelta(max(maxdays, 7))

        log = ['', '%s\tCleanup started...' % now]
        logger.info('Cleanup started ...')
        geQuery = Le('stiam.ro.effective', now - maxdays)
        query = SearchQuery(geQuery)
        brains = query.apply()

        intids = queryUtility(IIntIds)
        if not intids:
            logger.warn('No intids utility. Cleanup aborted.')
            return

        for index, docid in enumerate(brains):
            doc = intids.queryObject(docid, None)
            if doc is None:
                logger.exception(docid)
                continue

            logger.info('Delete %s', absoluteURL(doc, self.request))
            try:
                parent = doc.__parent__
                del parent[doc.__name__]
            except Exception, err:
                logger.exception(err)
                continue

            if index == 0:
                continue

            if index % 100 == 0:
                logger.info('Commit transaction %s', index)
                transaction.commit()

        logger.info('Cleanup finished.')
        log.append('%s\tCleanup finished.' % datetime.now(bucharest))
        return '\n'.join(log)

    def __call__(self, **kwargs):

        last_cleaned = getattr(self.context, 'last_cleaned', None)
        if not last_cleaned:
            self.context.last_cleaned = datetime.now(bucharest)
            transaction.commit()
            return self._cleanup(**kwargs)

        if not last_cleaned.tzinfo:
            args = last_cleaned.timetuple()[:6] + (0, utc)
            self.context.last_cleaned = datetime(*args)
            transaction.commit()

        cleanup_period = getattr(self.context, 'cleanup_period', 86340) # 23 hours and 59 minutes
        delta = datetime.now(bucharest) - self.context.last_cleaned
        if delta.days or (delta.seconds >= cleanup_period):
            return self._cleanup(**kwargs)

        logger.warn('Cleanup aborted! Please run again in %d seconds' % (
            cleanup_period - delta.seconds))
        return 'Cleanup aborted!'

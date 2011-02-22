import logging
import transaction
from datetime import datetime
from zope.component import queryUtility
from zope.publisher.browser import BrowserPage
from zope.intid.interfaces import IIntIds
from zope.app.file.interfaces import IImage
from z3c.blobfile.interfaces import IBlobImage

from z3c.indexer.query import Le
from z3c.indexer.search import SearchQuery

from stiamro import bucharest

logger = logging.getLogger('CLEANUP OLD IMAGES')

class Cleanup(BrowserPage):
    """ Remove all news items
    """
    def _cleanup(self, **kwargs):
        """ Cleanup thumbs
        """
        index = 0
        now = datetime.now(bucharest)
        logger.info('cleanup old images started ...')
        geQuery = Le('stiam.ro.effective', now)
        query = SearchQuery(geQuery)
        brains = query.apply()

        intids = queryUtility(IIntIds)
        if not intids:
            logger.warn('No intids utility. Cleanup aborted.')
            return index

        for docid in brains:
            try:
                doc = intids.getObject(docid)
            except KeyError, err:
                logger.exception(err)
                continue

            for image in doc.values():
                if not IImage.providedBy(image):
                    continue

                if IBlobImage.providedBy(image):
                    continue

                try:
                    del doc[image.__name__]
                except Exception, err:
                    logger.exception(err)
                    continue

                index += 1
                # Transaction commit
                if index % 20 == 0:
                    logger.info('Commit transaction %s', index)
                    transaction.commit()

        logger.info('Thumbs cleanup finished. Deleted %s thumbs.', index)
        return index

    def __call__(self, **kwargs):
        return "%s" % self._cleanup(**kwargs)

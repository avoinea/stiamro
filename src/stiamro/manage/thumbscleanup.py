import logging
import transaction
from datetime import datetime, timedelta
from zope.component import queryUtility
from zope.publisher.browser import BrowserPage
from zope.intid.interfaces import IIntIds
from zope.traversing.browser import absoluteURL
from zope.annotation.interfaces import IAnnotations
from zope.app.file.interfaces import IImage

from z3c.indexer.query import Le
from z3c.indexer.search import SearchQuery

from stiamro import utc, bucharest
logger = logging.getLogger('THUMBS CLEANUP')

class Cleanup(BrowserPage):
    """ Remove all news items
    """
    def _cleanup(self, **kwargs):
        """ Cleanup thumbs
        """
        index = 0
        if self.request:
            kwargs.update(self.request.form)
        maxdays = kwargs.get('days', 2)
        try:
            maxdays = int(maxdays)
        except Exception, err:
            maxdays = 2

        maxdays = timedelta(maxdays)
        now = datetime.now(bucharest)
        logger.info('Thumbs cleanup started ...')
        geQuery = Le('stiam.ro.effective', now - maxdays)
        query = SearchQuery(geQuery)
        brains = query.apply()

        intids = queryUtility(IIntIds)
        if not intids:
            logger.warn('No intids utility. Thumbs cleanup aborted.')
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

                anno = IAnnotations(image)
                for key in anno.keys():
                    key = str(key)
                    if key not in  ('album', 'thumbnail',
                                    'normal','large','icon','link'):
                        continue
                    index += 1

                    logger.info('%s: delete thumbs for %s',
                                index, absoluteURL(doc, self.request))
                    del anno[key]

                    # Transaction commit
                    if index % 20 == 0:
                        logger.info('Commit transaction %s', index)
                        transaction.commit()

        logger.info('Thumbs cleanup finished. Deleted %s thumbs.', index)
        return index

    def __call__(self, **kwargs):
        return "%s" % self._cleanup(**kwargs)

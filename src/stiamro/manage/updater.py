import logging
from datetime import datetime
from StringIO import StringIO
from persistent import Persistent
from zope.app.container.contained import Contained
from zope.interface import implements
from zope.publisher.browser import BrowserRequest
from zope.component import queryMultiAdapter
from zope.security.management import endInteraction
from interfaces import INewsUpdater
logger = logging.getLogger('UPDATER')

from stiamro import bucharest

class NewsUpdater(Persistent, Contained):
    """ News Updater used by lovely,remotetask to create cronjobs
    """
    implements(INewsUpdater)

    def __call__(self, service, input, *args, **kwargs):
        """ Run cronjob
        """
        # Pause updater in order to allow server to cleanup and zeopack
        now = datetime.now(bucharest)
        hour = now.hour
        if hour in (2, 3, 4):
            return 'Not in update interval'

        context = self.__parent__
        request = BrowserRequest(StringIO(), {})
        page = queryMultiAdapter((context, request), name=u'update')
        if not page:
            logger.exception('No update page found!')
            return 'No update page found'

        # XXX Don't know the side effects
        endInteraction()

        msg = page()
        logger.info(msg)
        return msg

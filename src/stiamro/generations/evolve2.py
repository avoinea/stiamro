""" Evolution 2
"""
import logging
from datetime import datetime
from zope.app.zopeappgenerations import getRootFolder
from lovely import remotetask
from lovely.remotetask.interfaces import ITaskService, ITask
from stiamro.content.interfaces import IPage
from stiamro.manage.updater import NewsUpdater

logger = logging.getLogger('stiamro.generation.2')

def evolve(context):
    """ Evolve
    """
    root = getRootFolder(context)
    site = root['stiam.ro']
    sm = site.getSiteManager()
    if 'cronjob4news' not in sm['default']:
        service = remotetask.TaskService()
        sm['default']['cronjob4news'] = service
        service = sm['default']['cronjob4news']
        sm.registerUtility(service, ITaskService, name="cronjob4news")
        logger.info('Registered utility cronjob4news')
    else:
        service = sm['default']['cronjob4news']

    # Add news updaters
    pages = site.values()

    sursa = site['sursa']
    now = datetime.now()
    minute = now.minute
    for page in pages:
        if not IPage.providedBy(page):
            continue

        sources = getattr(page, 'sources', '')
        if isinstance(sources, (str, unicode)):
            sources = sources.split('\n')

        for source in sources:
            server, news = source.split('/')
            rss = sursa[server][news]
            name = u'%s.%s.%s' % ('sursa', server, news)

            if 'updater' not in rss:
                logger.info('Adding updater for rss %s', name)
                updater = NewsUpdater()
                rss['updater'] = updater
                updater = rss['updater']
                sm.registerUtility(updater, ITask, name=name)
                service.addCronJob(name, (), minute=(minute,))
                minute += 7
                minute = minute % 60

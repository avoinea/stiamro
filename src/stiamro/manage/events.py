import logging
from random import randint
from datetime import datetime
from zope.component import getUtility
from zope.app.publication.interfaces import IBeforeTraverseEvent
from z3c.indexer.indexer import unindex
from z3c.indexer.indexer import index as z3c_index
from stiamro.content.interfaces import ISite
from updater import NewsUpdater
from lovely.remotetask.interfaces import ITask
from zope.intid import addIntIdSubscriber, removeIntIdSubscriber
from stiamro.generations.setup import Setup
from lovely.remotetask.interfaces import ITaskService
from zope.app.component.hooks import getSite

from allen.catalog.timeline.interfaces import ITimeline

from stiamro import bucharest

logger = logging.getLogger('EVENTS')

#
# print
#
def printEvent(obj, evt):
    if IBeforeTraverseEvent.providedBy(evt):
        return
    logger.info( "%s %s", repr(obj), repr(evt))

#
# stiamro.content.interfaces.ISite
#
def site_on_add(obj, evt):
    """ Handle site add
    """
    setup = Setup(obj, None)
    return setup()

#
# stiamro.content.interfaces.INewsItem
#
def newsitem_on_add(obj, evt):
    """ Handle newsitem add """

    try:
        addIntIdSubscriber(obj, evt)
        z3c_index(obj)
    except Exception, err:
        logger.exception(err)
    else:
        logger.debug('Successfully indexed using z3c.indexer')

    #timeline = getUtility(ITimeline, name=u'news.timeline')
    #timeline.index(obj)

def newsitem_on_change(obj, evt):
    """ Handle newsitem changes
    """
    try:
        z3c_index(obj)
    except Exception, err:
        logger.exception(err)
    else:
        logger.debug('Successfully re-indexed using z3c.indexer')


def newsitem_on_delete(obj, evt):
    """ Handle object delete
    """
    #timeline = getUtility(ITimeline, name=u'news.timeline')
    #timeline.unindex(obj)
    try:
        unindex(obj)
        removeIntIdSubscriber(obj, evt)
    except Exception, err:
        logger.exception(err)
    else:
        logger.debug('Successfully unindexed')
#
# stiamro.content.interfaces.INews
#
def news_on_add(obj, evt):
    """ Handle news add """
    obj['updater'] = NewsUpdater()
    updater = obj['updater']
#
# stiamro.manage.interfaces.INewsUpdater
#
def get_dotted_name(obj):
    """ Return dotted name relative to site
    """
    name = []
    while not ISite.providedBy(obj):
        name.append(obj.__name__)
        obj = obj.__parent__

    name.reverse()
    return '.'.join(name)
#
# Updater
#
def updater_on_add(obj, evt):
    """ Handle updater add """
    site = getSite()
    sm = site.getSiteManager()
    service = getUtility(ITaskService, name=u'cronjob4news')

    parent = obj.__parent__
    name = get_dotted_name(parent)

    sm.registerUtility(obj, ITask, name=name)
    now = datetime.now(bucharest)
    minute = (now.minute + randint(0, 30)) % 60
    jobid = service.addCronJob(name, (), minute=(minute,))
    obj.jobid = jobid
    logger.debug('Added cronjob: %s, name: %s', obj.jobid, name)

def updater_on_delete(obj, evt):
    """ Handle updater deletion """

    jobid = getattr(obj, 'jobid', None)
    if not jobid:
        return

    site = getSite()
    sm = site.getSiteManager()
    service = getUtility(ITaskService, name=u'cronjob4news')

    service.cancel(jobid)
    service.clean()

    parent = obj.__parent__
    name = get_dotted_name(parent)

    sm.unregisterUtility(obj, ITask, name=name)
    logger.debug('Removed cronjob: %s, name: %s', obj.jobid, name)

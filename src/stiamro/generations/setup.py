import logging
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds

from z3c.indexer import interfaces
from z3c.indexer.index import TextIndex
from z3c.indexer.index import FieldIndex
from z3c.indexer.index import SetIndex
from zope.publisher.browser import BrowserPage
from zope.app.component.site import SiteManagementFolder
from zope.app.component.site import LocalSiteManager
from zope.component import ComponentLookupError

from lovely.memcached.utility import MemcachedClient
from lovely.memcached.interfaces import IMemcachedClient
from lovely import remotetask

from stiamro.google.insights.content import Insights
from stiamro.google.insights.interfaces import IInsights

from allen.catalog.timeline.interfaces import ITimeline
from allen.catalog.timeline.timeline import Timeline

logger = logging.getLogger('stiamro.setup')

class Setup(BrowserPage):
    """ Setup site
    """
    def __call__(self, **kwargs):
        """ Setup catalog
        """
        site = self.context

        # Site manager
        try:
            sm = site.getSiteManager()
        except ComponentLookupError, err:
            sm = LocalSiteManager(site)
            site.setSiteManager(sm)

        # Catalog folder
        if 'catalog' not in sm:
            catalog = SiteManagementFolder()
            sm['catalog'] = catalog
            logger.info('Added catalog folder')

        # Intids utility
        if 'intids' not in sm['catalog']:
            intids = IntIds()
            sm['catalog']['intids'] = intids
            sm.registerUtility(intids, IIntIds)
            logger.info('Registered utility intids')

        # Setup text index
        if 'stiam.ro.text' not in sm['catalog']:
            textIndex = TextIndex()
            sm['catalog']['stiam.ro.text'] = textIndex
            sm.registerUtility(textIndex, interfaces.IIndex, name='stiam.ro.text')
            logger.info('Registered index stiam.ro.text')

        # Setup title index
        if 'stiam.ro.title' not in sm['catalog']:
            titleIndex = FieldIndex()
            sm['catalog']['stiam.ro.title'] = titleIndex
            sm.registerUtility(titleIndex, interfaces.IIndex, name='stiam.ro.title')
            logger.info('Registered index stiam.ro.title')

        # Setup description index
        if 'stiam.ro.description' not in sm['catalog']:
            descriptionIndex = TextIndex()
            sm['catalog']['stiam.ro.description'] = descriptionIndex
            sm.registerUtility(descriptionIndex, interfaces.IIndex, name='stiam.ro.description')
            logger.info('Registered index stiam.ro.description')

        # Setup updated index
        if 'stiam.ro.effective' not in sm['catalog']:
            updatedIndex = FieldIndex()
            sm['catalog']['stiam.ro.effective'] = updatedIndex
            sm.registerUtility(updatedIndex, interfaces.IIndex, name='stiam.ro.effective')
            logger.info('Registered index stiam.ro.effective')

        # Setup tags index
        if 'stiam.ro.tags' not in sm['catalog']:
            tagsIndex = SetIndex()
            sm['catalog']['stiam.ro.tags'] = tagsIndex
            sm.registerUtility(tagsIndex, interfaces.IIndex, name='stiam.ro.tags')
            logger.info('Registered index stiam.ro.tags')

        # Setup source index
        if 'stiam.ro.source' not in sm['catalog']:
            sourceIndex = FieldIndex()
            sm['catalog']['stiam.ro.source'] = sourceIndex
            sm.registerUtility(sourceIndex, interfaces.IIndex, name='stiam.ro.source')
            logger.info('Registered index stiam.ro.source')

        # Timeline
        if 'news.timeline' not in sm['catalog']:
            timeline = Timeline()
            sm['catalog']['news.timeline'] = timeline
            sm.registerUtility(timeline, ITimeline, name=u'news.timeline')
            logger.info('Registerd timeline utility')

        # Memcache
        if 'memcache' not in sm:
            memcache = MemcachedClient(servers=['127.0.0.1:16559'])
            sm['memcache'] = memcache
            sm.registerUtility(memcache, IMemcachedClient)

        # Google
        if 'google' not in sm:
            google = SiteManagementFolder()
            sm['google'] = google

        # Google Insights
        if 'insights' not in sm['google']:
            insights = Insights()
            sm['google']['insights'] = insights
            sm.registerUtility(insights, IInsights)

        # Cornjobs
        if 'cronjobs' not in sm:
            cronjobs = SiteManagementFolder()
            sm['cronjobs'] = cronjobs

        if 'news' not in sm['cronjobs']:
            task = remotetask.TaskService()
            sm['cronjobs']['news'] = task
            sm.registerUtility(task, remotetask.interfaces.ITaskService, 'cronjob4news')

        return 'Done'

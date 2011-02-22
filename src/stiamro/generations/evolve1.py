import logging
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding
from stiamro.content.interfaces import ISite, INewsItem
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds

from z3c.indexer import interfaces
from z3c.indexer.index import TextIndex
from z3c.indexer.index import FieldIndex
from z3c.indexer.index import ValueIndex
from z3c.indexer.index import SetIndex
from z3c.indexer.indexer import index as z3c_index

logger = logging.getLogger('stiamro.generation.1')

def evolve(context):
    """ Evolve
    """
    root = getRootFolder(context)
    site = root['stiam.ro']
    sm = site.getSiteManager()
    if 'intids' not in sm['default']:
        intids = IntIds()
        sm['default']['intids'] = intids
        sm.registerUtility(intids, IIntIds)
        logger.info('Registered utility intids')

    # Setup text index
    if 'stiam.ro.text' not in sm['default']:
        textIndex = TextIndex()
        sm['default']['stiam.ro.text'] = textIndex
        sm.registerUtility(textIndex, interfaces.IIndex, name='stiam.ro.text')
        logger.info('Registered index stiam.ro.text')

    # Setup title index
    if 'stiam.ro.title' not in sm['default']:
        titleIndex = FieldIndex()
        sm['default']['stiam.ro.title'] = titleIndex
        sm.registerUtility(titleIndex, interfaces.IIndex, name='stiam.ro.title')
        logger.info('Registered index stiam.ro.title')

    # Setup description index
    if 'stiam.ro.description' not in sm['default']:
        descriptionIndex = TextIndex()
        sm['default']['stiam.ro.description'] = descriptionIndex
        sm.registerUtility(descriptionIndex, interfaces.IIndex, name='stiam.ro.description')
        logger.info('Registered index stiam.ro.description')

    # Setup updated index
    if 'stiam.ro.effective' not in sm['default']:
        updatedIndex = FieldIndex()
        sm['default']['stiam.ro.effective'] = updatedIndex
        sm.registerUtility(updatedIndex, interfaces.IIndex, name='stiam.ro.effective')
        logger.info('Registered index stiam.ro.effective')

    # Setup tags index
    if 'stiam.ro.tags' not in sm['default']:
        tagsIndex = SetIndex()
        sm['default']['stiam.ro.tags'] = tagsIndex
        sm.registerUtility(tagsIndex, interfaces.IIndex, name='stiam.ro.tags')
        logger.info('Registered index stiam.ro.tags')

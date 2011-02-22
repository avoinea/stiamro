""" Evolution 2
"""
import logging
from datetime import datetime
from zope.app.zopeappgenerations import getRootFolder
from lovely import remotetask
from lovely.remotetask.interfaces import ITask
from stiamro.content.interfaces import IPage

logger = logging.getLogger('stiamro.generation.5')

def evolve(context):
    """ Evolve
    """
    root = getRootFolder(context)
    site = root['stiam.ro']

    for page in site.values():
        if not IPage.providedBy(page):
            continue

        if hasattr(page, 'last_updated'):
            logger.info('Deleting last_updated attr: %s', page)
            delattr(page, 'last_updated')
        if hasattr(page, 'update_period'):
            logger.info('Deleting update_period attr: %s', page)
            delattr(page, 'update_period')
        if hasattr(page, 'sources'):
            logger.info('Deleting sources attr: %s', page)
            delattr(page, 'sources')

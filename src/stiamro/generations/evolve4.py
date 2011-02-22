""" Evolution 2
"""
import logging
from datetime import datetime
from zope.app.zopeappgenerations import getRootFolder
from lovely import remotetask
from lovely.remotetask.interfaces import ITask
from stiamro.content.interfaces import IPage

logger = logging.getLogger('stiamro.generation.4')

def evolve(context):
    """ Evolve
    """
    root = getRootFolder(context)
    site = root['stiam.ro']
    sm = site.getSiteManager()
    service = sm['default']['cronjob4news']
    for jobid, value in service.jobs.items():
        name = value.task
        obj = sm.getUtility(ITask, name=name)
        obj.jobid = jobid
        logger.info('Set jobid: %s for local utility: %s', jobid, name)

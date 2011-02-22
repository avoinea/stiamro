from stiamro.content.interfaces import ISite
from zope.interface import implements
from zope.app.folder import Folder
from zope.dublincore.property import DCProperty

class Site(Folder):
    """ Site
    """
    implements(ISite)

    title = DCProperty('title')
    description = DCProperty('description')
    cleanup_period = 72000 # 20 hours
    last_cleaned = None

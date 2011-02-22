from stiamro.content.interfaces import ISource
from zope.interface import implements
from zope.app.folder import Folder
from zope.dublincore.property import DCProperty

class Source(Folder):
    """ Feeds server
    """
    implements(ISource)

    title = DCProperty('title')
    description = DCProperty('description')

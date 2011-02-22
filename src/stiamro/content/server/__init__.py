from stiamro.content.interfaces import IServer
from zope.interface import implements
from zope.app.folder import Folder
from zope.dublincore.property import DCProperty

class Server(Folder):
    """ Feeds server
    """
    implements(IServer)

    title = DCProperty('title')
    description = DCProperty('description')
    url = ''

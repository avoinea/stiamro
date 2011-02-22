from stiamro.content.interfaces import INewsItem
from zope.interface import implements
from zope.app.folder import Folder
from zope.dublincore.property import DCProperty

class NewsItem(Folder):
    """ NewsItem
    """
    implements(INewsItem)

    title = DCProperty('title')
    description = DCProperty('description')
    url = ''
    image = ''
    updated = None
    tags = []

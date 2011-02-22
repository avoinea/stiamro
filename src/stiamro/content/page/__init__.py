from stiamro.content.interfaces import IPage
from zope.interface import implements
from zope.app.folder import Folder
from zope.dublincore.property import DCProperty

class Page(Folder):
    """ Page
    """
    implements(IPage)

    title = DCProperty('title')
    description = DCProperty('description')
    tags = []
    max_items = 15
    order = 10

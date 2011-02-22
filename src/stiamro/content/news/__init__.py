from stiamro.content.interfaces import INews
from zope.interface import implements
from zope.app.folder import Folder
from zope.dublincore.property import DCProperty

class News(Folder):
    """ News
    """
    implements(INews)

    title = DCProperty('title')
    description = DCProperty('description')
    url = ''
    update_period = 600 # 10 Min

    # Public updater
    updated = None
    etag = ''
    last_updated = None

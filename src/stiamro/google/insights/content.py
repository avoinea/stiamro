from zope.interface import implements
from zope.app.folder import Folder
from zope.dublincore.property import DCProperty
from interfaces import IInsights

class Insights(Folder):
    """ Google Insights
    """
    implements(IInsights)

    title = DCProperty('title')
    description = DCProperty('description')
    email = ''
    password = ''

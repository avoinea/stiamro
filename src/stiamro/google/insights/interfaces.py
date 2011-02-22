from zope.interface import Interface
from zope import schema
from stiamro.content.interfaces import IContent

class IInsights(IContent):
    """ Google Insights
    """
    email = schema.TextLine(title=u'Google email')
    password = schema.Password(title=u'Google Password')

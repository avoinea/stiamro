from zope import schema
from zope.interface import Interface

class IExport(Interface):
    """ Export content
    """
    body = schema.Text(title=u"Body", readonly=True)

class IImport(Interface):
    """ Import content
    """
    body = schema.Text(title=u"Body", readonly=True)

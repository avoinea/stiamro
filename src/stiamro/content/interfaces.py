from zope.interface import Interface
from zope import schema
from allen.content.core.interfaces import IContent

#
# Site
#
class ISite(IContent):
    """ A container for sites
    """
    title = schema.TextLine(title=u'Titlu')
    description = schema.Text(title=u'Descriere', required=False)
    cleanup_period = schema.Int(title=u'Perioada de curatare (secunde)', required=True)
    last_cleaned = schema.Datetime(title=u"Ultima curatare", required=False)
#
# Sources folder
#
class ISource(IContent):
    """ Container for servers
    """
    title = schema.TextLine(title=u'Titlu')
    description = schema.Text(title=u'Descriere', required=False)
#
# Feed
#
class IServer(IContent):
    """ Feeds server
    """
    title = schema.TextLine(title=u'Titlu')
    description = schema.Text(title=u'Descriere', required=False)
    url = schema.TextLine(title=u'Server url')

class INews(IContent):
    """ News
    """
    title = schema.TextLine(title=u'Titlu')
    description = schema.Text(title=u'Descriere', required=False)
    url = schema.TextLine(title=u'URL')
    update_period = schema.Int(title=u'Perioada de actualizare (secunde)', required=True)

class INewsUpdater(Interface):
    updated = schema.Datetime(title=u"Ultima actualizare", required=False)
    etag = schema.TextLine(title=u"etag", required=False)
    last_updated = schema.Datetime(title=u"Ultima actualizare", required=False)

class INewsItem(IContent):
    """ News item
    """
    title = schema.TextLine(title=u'Titlu')
    description = schema.Text(title=u'Descriere')
    url = schema.TextLine(title=u'URL')
    updated = schema.Datetime(title=u"Ultima actualizare")
    tags = schema.List(title=u'Tags', value_type=schema.TextLine())
#
# Page
#
class IPage(IContent):
    """ View page
    """
    title = schema.TextLine(title=u'Titlu')
    description = schema.Text(title=u'Descriere', required=False)
    tags = schema.List(title=u'Tags', value_type=schema.TextLine())
    max_items = schema.Int(title=u"Stiri pe pagina", default=15)
    order = schema.Int(title=u"Pozitie", default=10)
#
# Sorting
#
class ISortedContent(Interface):
    """ Sort content
    """
    def children(interface=None, sort_by='title', reverse=False):
        """ Get sorted children by interface.
        """

from zope.viewlet.interfaces import IViewletManager
from z3c.layer.minimal import IMinimalBrowserLayer

class IStiamLayer(IMinimalBrowserLayer):
    """The Stiam layer interface"""

class IHead(IViewletManager):
    """ Header """

class IHeader(IViewletManager):
    """ """

class IToolbarTop(IViewletManager):
    """ Toolbar Top"""

class IToolbarBottom(IViewletManager):
    """ Toolbar Bottom"""

class ISidebar(IViewletManager):
    """ Sidebar """

class IContentTop(IViewletManager):
    """ Content header """

class IContentBottom(IViewletManager):
    """ Content footer """

class IFooter(IViewletManager):
    """ """

class IFoot(IViewletManager):
    """ """

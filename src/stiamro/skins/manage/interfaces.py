from zope.app.rotterdam import Rotterdam
from stiamro.skins.default.interfaces import IStiamLayer

class IManageLayer(Rotterdam, IStiamLayer):
    """The management layer interface"""

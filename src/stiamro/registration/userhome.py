from interfaces import IUserHome
from zope.app.container.btree import BTreeContainer
from zope.interface import implements

class UserHome(BTreeContainer):
    implements(IUserHome)
    __doc__ = IUserHome.__doc__

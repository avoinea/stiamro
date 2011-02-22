from zope.interface import Interface

class ILastUpdated(Interface):
    """ Adapter to get context last updated
    """
    def __call__(self):
        """ Run
        """

class IText(Interface):
    """ Utility to handle text
    """

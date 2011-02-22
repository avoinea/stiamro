import operator
from zope.interface import implements
from interfaces import ISortedContent

class SortedContent(object):
    implements(ISortedContent)

    def __init__(self, context):
        self.context = context

    def children(self, interface=None, sort_by='title', reverse=False):
        """ Get sorted children
        """
        if interface:
            children = [child for child in self.context.values()
                        if interface.providedBy(child)]
        else:
            children = [child for child in self.context.values()]

        children.sort(key=operator.attrgetter(sort_by), reverse=reverse)
        for child in children:
            yield child

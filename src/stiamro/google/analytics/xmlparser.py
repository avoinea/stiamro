import logging
from xml.dom import minidom
from zope.interface import implements
from interfaces import IXMLParser

logger = logging.getLogger('eea.google.analytics')

class XMLParser(object):
    """ See interface
    """
    implements(IXMLParser)

    def __call__(self, xml):
        dom = minidom.parseString(xml)
        entries = dom.getElementsByTagName('entry')
        for entry in entries:
            dimensions = {}
            metrics = {}
            for prop in entry.childNodes:
                if prop.nodeName == u'dxp:dimension':
                    name = prop.getAttribute('name')
                    dimensions[name] = prop.getAttribute('value')
                elif prop.nodeName == u'dxp:metric':
                    name = prop.getAttribute('name')
                    value = prop.getAttribute('value')
                    metrics[name] = value
            yield dimensions, metrics

""" Importers
"""
import base64
import logging
import transaction
from elementtree.ElementTree import XMLTreeBuilder, ElementTree

from zope import schema
from zope import event
from zope.app.form.interfaces import IInputWidget
from zope.interface import implements, providedBy
from zope.component import queryMultiAdapter
from stiamro.xml.interfaces import IImport
from stiamro.content.interfaces import INews
from zope.lifecycleevent import ObjectModifiedEvent

logger = logging.getLogger('stiam.ro.import')

CDATA = "<![CDATA[%s]]>"

class ImportContent(object):
    """ Import content
    """
    implements(IImport)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def child(self, element):
        """ Child importer
        """
        name = element.get('name')
        if not name:
            raise AttributeError('No name provided for object')

        if name not in self.context:
            factory = element.get('factory')
            if not factory:
                raise AttributeError('No factory provided for object %s' % name)

            factory = factory.split('.')
            klass = factory.pop()
            module = '.'.join(factory)
            module = __import__(module, globals(), locals(), [klass])
            factory = getattr(module, klass)

            logger.debug('Adding type %s: %s', klass, name)
            child = factory()
            self.context[name] = child
        else:
            child = self.context[name]

        importer = queryMultiAdapter((child, self.request), IImport)
        if importer:
            importer.body = element

    def attribute(self, element):
        """ Attribute importer
        """
        for iface in providedBy(self.context).flattened():
            idx = iface.__identifier__
            if idx.startswith('stiamro'):
                break

        name = element.get('name')
        if not name:
            raise AttributeError('Missing name attribute for tag <property>')

        field = iface.get(name, None)
        if not field:
            return

        elements = element.getchildren()
        if elements:
            value = [item.text for item in elements]
        else:
            widget = queryMultiAdapter((field, self.request), IInputWidget)
            value = widget._toFieldValue(element.text)

        if not value:
            return

        logger.debug('Set attribute %s: %s', name, value)
        field.set(self.context, value)

    def body(self, xml):
        """ Body importer
        """

        if isinstance(xml, (str, unicode)):
            parser = XMLTreeBuilder()
            parser.feed(xml)
            tree = parser.close()
            tree = ElementTree(tree)
            elem = tree.getroot()
        else:
            elem = xml

        if elem.tag != 'object':
            raise AttributeError('Invalid xml root element %s' % elem.tag)

        name = elem.get('name')
        if not name:
            raise AttributeError('No name provided for object')

        if hasattr(self.context, '__name__') and (name != self.context.__name__):
            raise AttributeError(('XML root object name %s '
                'should match context name %s') % (name, self.context.__name__))

        for child in elem.getchildren():
            if child.tag == 'property':
                self.attribute = child
            elif child.tag == 'object':
                self.child = child

        event.notify(ObjectModifiedEvent(self.context))

        if INews.providedBy(self.context):
            logger.info('Commit transaction import for %s' % getattr(
                self.context, '__name__', '(no name)'))
            transaction.commit()

    body = property(None, body)
    child = property(None, child)
    attribute = property(None, attribute)

class ImportImage(ImportContent):
    """ Image
    """
    def attribute(self, element):
        if not element.text:
            return

        name = element.get('name')
        if name == 'contentType':
            self.context.contentType = element.text
        if name == 'data':
            text = element.text
            text = text.replace('<![CDATA[', '', 1)
            text.strip(']]>')
            text = base64.decodestring(text)
            self.context.data = text

    attribute = property(None, attribute)

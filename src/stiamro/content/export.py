""" Export
"""
import base64
import logging
from zope import datetime as zdatetime
from datetime import datetime
from elementtree.ElementTree import Element, SubElement

from zope import schema

from zope.interface import implements, providedBy
from zope.component import queryMultiAdapter
from zope.app.form.interfaces import IDisplayWidget

from stiamro.xml.interfaces import IExport
from stiamro.content.interfaces import IContent

CDATA = "<![CDATA[%s]]>"
logger = logging.getLogger('stiam.ro.export')

class ExportContent(object):
    """ Export Content
    """
    implements(IExport)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def children(self):
        """ Children
        """
        logger.info('Export %s children of %s', len(self.context), self.context.__name__)
        for child in self.context.values():
            exporter = queryMultiAdapter((child, self.request), IExport)
            if not exporter:
                continue
            body = exporter.body
            if not body:
                continue
            yield body

    @property
    def properties(self):
        """ Export properties
        """
        for iface in providedBy(self.context).flattened():
            try:
                idx = iface.__identifier__
            except Exception, err:
                continue
            if idx.startswith('stiamro'):
                break

        fields = schema.getFieldsInOrder(iface)
        for name, field in fields:
            widget = queryMultiAdapter((field, self.request), IDisplayWidget)
            widget.setRenderedValue(field.get(self.context))

            attr = widget()
            prop = Element('property', name=name)

            if isinstance(widget._data, (list, tuple)):
                for item in widget._data:
                    subelement = SubElement(prop, 'element')
                    subelement.text = str(item)
            elif isinstance(widget._data, datetime):
                time = zdatetime.time(widget._data.isoformat())
                prop.text = zdatetime.rfc1123_date(time)
            else:
                prop.text = attr

            yield prop

    @property
    def body(self):
        """ Body exporter
        """
        klass = self.context.__class__
        factory = '.'.join((klass.__module__, klass.__name__))
        element = Element('object', name=self.context.__name__,
                          factory=factory)

        for prop in self.properties:
            element.append(prop)

        for child in self.children:
            element.append(child)

        return element

class ExportNewsItem(ExportContent):
    """ Export News Item
    """
    implements(IExport)

    @property
    def children(self):
        """ Children
        """
        return []

class ExportImage(ExportContent):
    """ Export Image
    """
    implements(IExport)

    @property
    def children(self):
        """ Children
        """
        return []

    @property
    def properties(self):
        """ Export properties
        """
        contentType = self.context.contentType
        prop = Element('property', name='contentType')
        prop.text = contentType
        yield prop

        data = self.context.data
        prop = Element('property', name='data')
        data = base64.encodestring(data)
        prop.text = CDATA % data
        yield prop

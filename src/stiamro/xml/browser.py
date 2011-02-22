import logging
from elementtree.ElementTree import ElementTree
from StringIO import StringIO
from zope.component import queryMultiAdapter
from zope.publisher.browser import BrowserPage
from interfaces import IExport, IImport

logger = logging.getLogger('stiam.ro.xml')

class Export(BrowserPage):
    """ Export View
    """
    def __call__(self, **kwargs):
        xml = """<?xml version="1.0" encoding="UTF-8"?>"""
        exporter = queryMultiAdapter((self.context, self.request), IExport)
        if not exporter:
            return xml

        body = exporter.body
        if not isinstance(body, ElementTree):
            body = ElementTree(body)

        out = StringIO()
        body.write(out)
        out.seek(0)
        xml += out.read()

        self.request.response.setHeader('content-type', 'text/xml')
        return xml

class Import(BrowserPage):
    """ Import
    """
    status = ''

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)
        xmlfile = kwargs.get('xmlfile', '')
        if not xmlfile:
            return self.index()

        xml = xmlfile.read()
        importer = queryMultiAdapter((self.context, self.request), IImport)
        if not importer:
            self.status = ('!!! Could not import XML as there is no '
                           'stiamro.xml.interfaces.IImport adapter for '
                           'this context !!!')
            return self.index()

        try:
            importer.body = xml
        except Exception, err:
            logger.exception(err)
            self.status = err
        else:
            self.status = 'XML succesfully imported.'

        return self.index()

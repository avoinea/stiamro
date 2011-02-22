from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.basicskin.standardmacros import StandardMacros as BaseMacros

class StiamMacros(BrowserView):
    template = ViewPageTemplateFile('zpt/stiam.pt')

    def __getitem__(self, key):
        return self.template.macros.get(key, self.template.macros['page'])

class StandardMacros(BaseMacros):
    macro_pages = ('stiam_macros',)

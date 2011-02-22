from zope.publisher.browser import BrowserPage

class View(BrowserPage):
    def __call__(self, **kwargs):
        return "%s" % len(self.context)

class IndexView(BrowserPage):
    def __call__(self, **kwargs):
        return "%s" % self.context.documentCount()

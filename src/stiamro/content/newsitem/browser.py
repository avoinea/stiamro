from zope.app import zapi
from zope.component import getMultiAdapter, getUtility
from zope.formlib.form import Fields, PageAddForm, PageEditForm, applyChanges
from zope.app.container.interfaces import INameChooser
from zope.app.file.interfaces import IImage

from stiamro.content.interfaces import INewsItem, ISite, IServer
from stiamro.content.newsitem import NewsItem
from zope.publisher.browser import BrowserPage
from zope.traversing.browser import absoluteURL

from stiamro.utils.interfaces import IText

class NewsItemAddPage(PageAddForm):
    """ Add a News
    """
    form_fields = Fields(INewsItem)
    def create(self, data):
        ob = NewsItem()

        title = data.get('title', 'stire')
        uid = INameChooser(self.context).chooseName(title, ob)
        setattr(ob, '_tmp_id', uid)
        applyChanges(ob, self.form_fields, data)
        return ob

    def add(self, obj):
        name = getattr(obj, '_tmp_id', 'server')
        delattr(obj, '_tmp_id')
        self.context[name] = obj
        self._finished_add = True
        return obj

    def nextURL(self):
        return "."

class NewsItemEditPage(PageEditForm):
    form_fields = Fields(INewsItem)

class NewsItemView(BrowserPage):
    """ Newsitem view
    """
    @property
    def date(self):
        """ Format date
        """
        date = self.context.updated
        return date.strftime('%Y/%m/%d %H:%M:%S')

    def thumbnail(self, context=None, size='thumbnail', from_parent=False):
        if not context:
            context = self.context

        for key, doc in context.items():
            if key == 'icon.png':
                continue
            if not IImage.providedBy(doc):
                continue

            scale = getMultiAdapter((doc, self.request), name=u'scale')
            try:
                thumb = scale.publishTraverse(self.request, size)
            except Exception, err:
                thumb = ''
            if thumb and thumb.getSize():
                return zapi.absoluteURL(doc, self.request)

        if from_parent:
            if not ISite.providedBy(context):
                return self.thumbnail(context.__parent__, size, from_parent)
        return ''

    @property
    def relative_id(self):
        url = getMultiAdapter((self.context, self.request), name=u'absolute_url')
        name = '/'.join([x.get('name', '') for x in url.breadcrumbs()])
        return name

    @property
    def favicon(self):
        # Get server
        context = self.context.__parent__.__parent__
        if not IServer.providedBy(context):
            return ''

        icon = context.get('icon.png', None)
        if not icon:
            return ''

        return absoluteURL(icon, self.request)

    @property
    def title(self):
        title = self.context.title
        cut = getattr(self, 'cuttext', 0)
        # XXX Use more descriptive method to see which context you are
        util = getUtility(IText)
        if not cut:
            util = getUtility(IText)
            return util.translate(title)

        # XXX Listing context
        return util.truncate_length(self.context.title, 140, 10)

    @property
    def description(self):
        description = self.context.description
        cut = getattr(self, 'cuttext', 0)
        util = getUtility(IText)
        # XXX Use more descriptive method to see which context you are
        if not cut:
            return util.translate(description)
        return util.truncate_length(description, 400, 20)

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)
        self.cuttext = kwargs.get('cuttext', 0)
        return self.index()

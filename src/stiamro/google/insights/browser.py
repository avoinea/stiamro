from difflib import SequenceMatcher
import operator
import logging
from zope.component import getMultiAdapter
from zope.formlib.form import Fields, PageEditForm
from zope.publisher.browser import BrowserPage

from z3c.indexer.search import SearchQuery
from z3c.indexer.query import TextQuery

from allen.utils.cache import servercache
from interfaces import IInsights
from api import Insight, GLogin
logger = logging.getLogger('GOOGLE INSIGHTS')

class EditPage(PageEditForm):
    form_fields = Fields(IInsights)

class View(BrowserPage):
    """ Insights view
    """
    _report = {}

    @property
    def report(self):
        if self._report:
            return self._report

        try:
            login = GLogin(self.context.email, self.context.password)
            data = Insight(login())
            data.get_report('RO', 'week')
            self._report = data.get_stat('rising')
        except Exception, err:
            logger.exception(err)
        return self._report

    @servercache
    def keywords(self):
        report = self.report.items()
        report.sort()
        keywords = [item[0] for index, item in report]

        try:
            hot = open('/var/local/edw/stiam/www/var/stiamro.hot', 'r')
        except Exception:
            return keywords
        else:
            tags = hot.read()
            hot.close()

        tags = tags.splitlines()
        tags = [tag.strip() for tag in tags if tag.strip()]
        tags.extend(key for key in keywords if key not in tags)
        return tags

    @property
    def etag(self):
        etag = getMultiAdapter((self.context, self.request), name=u'index.etag')
        etag = etag(insights=1)
        return etag

    @property
    def items(self):
        tags = self.keywords()
        index = 0
        res = {}
        for tag in tags:
            query = TextQuery('stiam.ro.text', tag)
            query = SearchQuery(query)
            brains = query.searchResults(sort_index='stiam.ro.effective',
                                         reverse=True, limit=5)
            res.update(dict((brain.__name__, brain) for brain in brains))
        res = res.values()

        # First item is generator length
        yield len(res)

        res.sort(key=operator.attrgetter('updated'), reverse=True)
        duplicate = ""
        for brain in res:
            if index >= 15:
                raise StopIteration

            # Remove duplicates
            title = getattr(brain, "title", "")
            s = SequenceMatcher(lambda x: x == " ", title, duplicate)
            if s.ratio() > 0.6:
                continue

            duplicate = title
            index += 1
            yield brain

    def __call__(self, **kwargs):
        return self.index()

class Portlet(BrowserPage):
    """ Display content as a 10 items portlet.
    """
    def news(self, max_items=10):
        """ Return news items
        """
        view = getMultiAdapter((self.context, self.request), name=u'content.html')
        index = 0
        for newsitem in view.items:
            if index > max_items:
                raise StopIteration
            index += 1
            yield newsitem

    def thumbnail(self, newsitem):
        """ Return icon
        """
        index = getMultiAdapter((newsitem, self.request), name=u'index.html')
        thumb = index.thumbnail(from_parent=True)
        if thumb:
            return thumb
        return ''

    @property
    def etag(self):
        """ Used by servercache decorator
        """
        etag = getMultiAdapter((self.context, self.request), name=u'index.etag')
        etag = etag(insights_portlet=1)
        return etag

    def relative_id(self, newsitem):
        view = getMultiAdapter((newsitem, self.request), name=u'index.html')
        return view.relative_id

    @servercache
    def __call__(self, **kwargs):
        return self.index()

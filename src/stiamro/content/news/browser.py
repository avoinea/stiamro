import time
import re
import logging
import urllib2
import feedparser
from difflib import SequenceMatcher
from datetime import datetime
from zope.component import getMultiAdapter
from zope.datetime import parseDatetimetz
from zope.formlib.form import Fields, PageAddForm, PageEditForm, applyChanges
from zope.app.container.interfaces import INameChooser
from zope.publisher.browser import BrowserPage
from z3c.blobfile.image import Image
from zope.app.container.interfaces import INameChooser

from stiamro import bucharest, utc
from stiamro.content.interfaces import INews
from stiamro.content.news import News
from BeautifulSoup import BeautifulSoup
from zope.traversing.browser.absoluteurl import absoluteURL
logger = logging.getLogger('NEWS')

from z3c.indexer.search import SearchQuery
from z3c.indexer.query import Eq, AnyOf

from allen.utils.cache import servercache

class NewsAddPage(PageAddForm):
    """ Add a News
    """
    form_fields = Fields(INews)
    def create(self, data):
        ob = News()

        title = data.get('title', 'stiri')
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
        return "add_news.html"

class NewsEditPage(PageEditForm):
    form_fields = Fields(INews)

class NewsUpdatePage(BrowserPage):
    """ Update news items
    """
    def add_image_from_enclosures(self, container, enclosures):
        """ Add image from enclosures
        """
        for enclosure in enclosures:
            enc_type = enclosure.get('type', '')
            if 'image' not in enc_type:
                continue
            enc_href = enclosure.get('href', '')
            if not enc_href:
                continue

            enc_href = enc_href.split('?')[0]
            enc_id = enc_href.split('/')[-1]
            try:
                conn = urllib2.urlopen(enc_href)
                data = conn.read()
            except Exception, err:
                logger.exception(err)
                continue
            if data:
                logger.info('Add image %s in %s',
                             enc_id, absoluteURL(container, self.request))
                container[enc_id] = Image(data)
            return container[enc_id]
        return None

    def add_image_from_summary(self, container, summary):
        """ Add image from summary
        """
        summary = summary.replace('\n', ' ')
        pattern = re.compile(r'\<img.*src=\"(?P<imagelink>.+?)\"')
        found = pattern.search(summary)
        if not found:
            return None
        image_link = found.group('imagelink')
        image_link = image_link.split('?')[0]
        image_path = image_link.split('/')
        image_id = image_path[-1] or image_path[-2]

        # Adds
        if image_link.startswith('http://core.ad20.net'):
            return None

        # Sport.ro
        if image_link.endswith('thumb_size3.jpg'):
            image_link = image_link.replace('thumb_size3.jpg', 'thumb_size1.jpg')
        if image_link.endswith('size3.jpg'):
            image_link = image_link.replace('size3.jpg', 'size1.jpg')
        try:
            conn = urllib2.urlopen(image_link)
        except urllib2.HTTPError, err:
            logger.exception('Image url: %s; Error: %s', image_link, err)
            return None
        data = conn.read()
        if data:
            logger.info('Add image %s in %s',
                         image_id, absoluteURL(container, self.request))
            container[image_id] = Image(data)
            return container[image_id]
        return None

    def add_image(self, container, entry):
        """ Try to add image in container
        """
        # Get image from enclosure
        enclosures = entry.get('enclosures', [])
        image = self.add_image_from_enclosures(container, enclosures)
        if image:
            return image

        # Get image from description
        summary = entry.get('summary', '')
        image = self.add_image_from_summary(container, summary)
        if image:
            return image

        return None

    def add_newsitem(self, entry):
        """ Add news item
        """
        title = entry.get('title', '')
        title = title.replace('&nbsp;', ' ').strip()

        description = BeautifulSoup(entry.get('summary', ''))
        description = ''.join([e for e in description.recursiveChildGenerator()
                               if isinstance(e,unicode)]).strip()

        # Descopera.ro
        index = description.find('Citeste tot articolul')
        if index != -1:
            description = description[:index]

        if not (title and description):
            return None

        url = entry.get('link', '#').strip()
        # Skip existing news
        uid = INameChooser(self.context).chooseName(title, None)
        try:
            newsitem = self.context[uid]
        except Exception, err:
            pass
        else:
            return newsitem

        add_page = getMultiAdapter((self.context, self.request),
                                   name=u'add_newsitem.html')

        updated = entry.get('updated', None)
        if not updated:
            updated = self.context.updated or datetime.now(bucharest)
        else:
            updated = parseDatetimetz(updated)
        query = {
            'title': title,
            'description': description,
            'url': url,
            'updated': updated,
            'tags': [self.context.__name__]
        }

        logger.info('Add newsitem %s in %s', uid, absoluteURL(
            self.context, self.request))

        try:
            newsitem = add_page.createAndAdd(query)
        except Exception, err:
            logger.exception(err)
            return None
        else:
            self.add_image(newsitem, entry)
        return newsitem

    def _update(self):
        """ Run updater
        """
        url = self.context.url
        etag = self.context.etag or None
        updated = self.context.updated
        if not isinstance(updated, datetime):
            updated = None
        else:
            updated = updated.timetuple()

        data = feedparser.parse(url, etag=etag, modified=updated)
        # No change
        if data.get('status', None) == 304:
            return "No changes made until last update"

        if data.get('etag', None):
            self.context.etag = etag

        last_updated = data.get('modified', None)
        if isinstance(last_updated, time.struct_time) and len(last_updated) >= 6:
            args = last_updated[:6] + (0, utc)
            self.context.updated = datetime(*args)
        else:
            self.context.updated = datetime.now(bucharest)

        for entry in data.get('entries', ()):
            self.add_newsitem(entry)

        return '%s\t%s\tUPDATED' % (
            datetime.now(bucharest).strftime('%d-%m-%Y %H:%M'),
            absoluteURL(self.context, self.request)
        )

    def __call__(self, **kwargs):
        """ Call
        """
        # Initial call
        last_updated = self.context.last_updated
        if not last_updated:
            self.context.last_updated = datetime.now(bucharest)
            return self._update()
        elif not last_updated.tzinfo:
            args = last_updated.timetuple()[:6] + (0, utc)
            last_updated = datetime(*args)

        # Call after update period
        now = datetime.now(bucharest)
        delta = now - last_updated
        update_period = self.context.update_period
        if delta.seconds >= update_period:
            self.context.last_updated = datetime.now(bucharest)
            return self._update()

        # Call before update period
        return '%s\t%s\tNOT UPDATED' % (
            datetime.now(bucharest).strftime('%d-%m-%Y %H:%M'),
            self.context.__name__
        )

class Content(BrowserPage):
    """ Content
    """
    @property
    def items(self):
        source = self.context.__parent__.__name__
        source = Eq('stiam.ro.source', source)

        tags = [self.context.__name__]
        tags = AnyOf('stiam.ro.tags', tags)

        query = SearchQuery(source).And(tags)
        brains = query.searchResults(sort_index='stiam.ro.effective',
                                     reverse=True, limit=30)

        duplicate = ""
        index = 0
        for brain in brains:
            if index >= 15:
                raise StopIteration

            title = getattr(brain, "title", "")
            s = SequenceMatcher(lambda x: x == "", title, duplicate)
            if s.ratio() > 0.6:
                continue

            duplicate = title
            index += 1
            yield brain

    @property
    def etag(self):
        etag = getMultiAdapter((self.context, self.request), name=u'index.etag')
        return etag(server=self.context.__parent__.__name__)

    @servercache
    def __call__(self, **kwargs):
        return self.index()

class View(Content):
    """ View
    """
    def __call__(self, **kwargs):
        return self.index()

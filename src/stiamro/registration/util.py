from zope.app.component.hooks import getSite
from zope.security.management import getInteraction
from zope.traversing.browser.absoluteurl import absoluteURL


def get_site_url(request=None):
    if request == None:
        request = getInteraction().participations[0]
    return absoluteURL(getSite(), request)

def get_homefolder(principal):
    return getSite()[principal.id]

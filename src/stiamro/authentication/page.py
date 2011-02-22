from stiamro.registration.util import get_site_url
from zope.app.security.interfaces import IUnauthenticatedPrincipal, \
    IAuthentication
from zope.component import getUtility
from zope.publisher.browser import BrowserPage

class LoginPage(BrowserPage):
    def __call__(self):
        if not IUnauthenticatedPrincipal.providedBy(self.request.principal):
            self.request.response.redirect(get_site_url())
            return ""
        return self.index()

class LogoutPage(BrowserPage):

    def __call__(self):
        getUtility(IAuthentication).logout(self.request)
        site_url = get_site_url(self.request)
        self.request.response.redirect("%s" % site_url)
        return ""

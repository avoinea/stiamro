##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import sha
import datetime
from config import EMAIL_TEMPLATE
from interfaces import IConfirmationEmail, IRegistration, \
    IRegistrations
from util import get_site_url
from persistent import Persistent
from zope.component import adapter
from zope.app.authentication.principalfolder import InternalPrincipal
from zope.app.container.btree import BTreeContainer
from zope.app.container.contained import Contained
from zope.app.container.interfaces import INameChooser
from zope.app.security.interfaces import IAuthentication
from zope.component import adapts, getUtility
from zope.interface import implements
from zope.app.component.hooks import getSite
from userhome import UserHome
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.sendmail.interfaces import IMailDelivery
from zope.app.container.interfaces import IObjectAddedEvent

from stiamro import bucharest

class Registration(Contained, Persistent):

    implements(IRegistration)

    def __init__(self, hash, email, data):
        self.hash = hash
        self.email = email
        self.data = data

class Registrations(BTreeContainer):

    implements(IRegistrations)

    def _createHash(self, email, data=None):
        return sha.new(email + datetime.datetime.now(bucharest).isoformat()).hexdigest()

    def register(self, email, data=None, factory=Registration):
        """Create a new registration for the given email address and data."""
        hash = self._createHash(email, data)
        self[hash] = registration = factory(hash, email, data)
        return registration

    def confirm(self, hash):
        """Confirm the registration identified by the hash."""
        registration = self[hash]
        data = registration.data
        util = getUtility(IAuthentication)
        members = util['members']
        username = data['username']
        if username in members:
            raise ValueError("Username already registered")
        ip = InternalPrincipal(login=username,
                               password=data['password'],
                               title=username)
        #XXX: there's a possibility for subtle bugs here
        name = INameChooser(members).chooseName(username, ip)
        members[name] = ip

        site = getSite()
        site[name] = uh = UserHome()
        IPrincipalRoleManager(uh).assignRoleToPrincipal('stiam.ro.Owner', username)
        del self[hash]

class ConfirmationEmail(object):
    """A basic confirmation email."""

    adapts(IRegistration)
    implements(IConfirmationEmail)

    addr_from = "Stiam .RO <contact@stiam.ro>"
    confirmation_url = "%s/@@confirm.html?hash=%s"

    def __init__(self, registration):
        self.message = EMAIL_TEMPLATE % {
            'to': registration.email,
            'from': self.addr_from,
            'link': self.confirmation_url % (get_site_url(), registration.hash)}

@adapter(IRegistration, IObjectAddedEvent)
def send_registration_mail(registration, event):
    """Listen for a registration and send a mail to the user, asking for
    confirmation.
    """
    email = IConfirmationEmail(registration)
    mailer = getUtility(IMailDelivery, name="stiam.ro.mailer")
    mailer.send(email.addr_from, [registration.email], email.message)

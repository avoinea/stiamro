from i18n import _
from zope.interface import Interface, invariant, Attribute
from zope import schema

class IRegistrationSchema(Interface):
    username = schema.TextLine(
        title=_(u"Utilizator"),
        description=_(u"Introdu numele de utilizator dorit"),
        required=True,
    )
    password = schema.Password(
        title=_(u"Parola"),
        description=_(u"Introdu o parola de minim 5 caractere"),
        required=True,
    )
    password_check = schema.Password(
        title=_(u"Verificare parola"),
        description=_(u"Repeta parola"),
        required=True,
    )
    email = schema.TextLine(
        title=_(u"Adresa de email"),
        description=_(u"Adresa de email unde vom trimite un link pentru confirmare"),
        required=True,
    )

    @invariant
    def check_password(self):
        if self.password and self.password_check:
            if self.password != self.password_check:
                raise ValidationError("Ai introdus gresit parola in cel de-al doilea camp")

class IRegistrations(Interface):
    """Provide self-registration functionality.

    Registrations are done for users giving their email address and
    possibly more data.

    A registration requires confirmation by the user. For this we
    send an email containing a confirmation link to his address.

    Upon opening the link a RegistrationConfirmedEvent is sent out
    and the application can perform whatever is necessary to active
    the user's account.

    After the successful confirmation the intermediate registration
    object is deleted.

    """

    def register(email, data=None):
        """Create a new registration for the given email address and
        data.

        Sends out an ObjectAddedEvent for the newly created
        IRegistration object.
        """

    def confirm(hash):
        """Confirm the registration identified by the hash.

        If successful sends out an IRegistrationConfirmed event.
        """

class IRegistration(Interface):
    """A registration."""

    hash = schema.BytesLine(title=u"A hash identifying this registration",)
    email = schema.TextLine(title=u"The email for sending the confirmation mail to.")
    data = Attribute(u"Application-specific registration data.")


class IConfirmationEmail(Interface):
    """An email to confirm a registration."""

    message = Attribute("A string containing an RFC 2822 message.")

class IUserHome(Interface):
    """A home for the items of one user"""

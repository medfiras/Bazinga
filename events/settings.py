"""Settings for the ``events`` app."""
from django.conf import settings

gettext = lambda s: s

REQUIRED_FIELDS_CHOICES = getattr(
    settings,
    'EVENT_RSVP_REQUIRED_FIELDS_CHOICES',
    (
        ('name', gettext('Name')),
        ('email', gettext('Email')),
        ('phone', gettext('Phone')),
    )
)

GUEST_FORM = getattr(settings, 'EVENT_RSVP_GUEST_FORM',
                     'events.forms.base.GuestForm')
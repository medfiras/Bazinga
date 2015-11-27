"""Settings for the ``events`` app."""
from django.conf import settings

gettext = lambda s: s

REQUIRED_FIELDS_CHOICES = getattr(
    settings,
    'EVENT_REQUIRED_FIELDS_CHOICES',
    (
        ('name', gettext('Name')),
        ('email', gettext('Email')),
        ('phone', gettext('Phone')),
    )
)

GUEST_FORM = getattr(settings, 'EVENT_GUEST_FORM', 'events.forms.base.GuestForm')


EVENTS_IMAGE_DEFAULT = getattr(settings, 'EVENTS_IMAGE_DEFAULT', 'identicon')

EVENTS_IMAGE_SIZE = getattr(settings, 'EVENTS_IMAGE_SIZE', 80)

EVENTS_IMAGE_CROP_TYPE = getattr(settings, 'EVENTS_IMAGE_CROP_TYPE', 'smart')

EVENTS_IMAGE_PATH = getattr(settings, 'EVENTS_IMAGE_PATH', 'events/')
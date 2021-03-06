"""Models for the ``Events`` application."""
from django import forms
from django.core import exceptions
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import date, slugify
from django.utils import timezone
from django.utils.text import capfirst
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from .settings import REQUIRED_FIELDS_CHOICES

from easy_thumbnails.fields import ThumbnailerImageField
from events import settings as events_settings

from events.utils import generate_sha1, get_datetime_now

from django.dispatch import receiver
from django.db.models.signals import post_save
from .tasks import *


def upload_to_mugshot(instance, filename):
    """
    Uploads an image for an event and saving it
    under unique hash for the image. This is for privacy reasons so others
    can't just browse through the mugshot directory.
    """
    extension = filename.split('.')[-1].lower()
    salt, hash = generate_sha1(instance.pk)
    path = events_settings.EVENTS_IMAGE_PATH % {'date_now': get_datetime_now().now()}
    return '%(path)s%(hash)s.%(extension)s' % {'path': path,
                                               'hash': hash[:10],
                                               'extension': extension}


class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple

    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        return value


class MultiSelectField(models.Field):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "CharField"

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def formfield(self, **kwargs):
        # don't call super, as that overrides default widget if it has choices
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text, 'choices': self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_prep_value(self, value):
        return value

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if isinstance(value, basestring):
            return value
        elif isinstance(value, list):
            return ",".join(value)

    def to_python(self, value):
        if value is not None:
            return value if isinstance(value, list) else value.split(',')
        return ''

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            func = lambda self, fieldname = name, choicedict = dict(
                self.choices): ",".join([choicedict.get(
                    value, value) for value in getattr(self, fieldname)])
            setattr(cls, 'get_%s_display' % self.name, func)

    def validate(self, value, model_instance):
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for opt_select in value:
            if opt_select not in arr_choices:
                raise exceptions.ValidationError(
                    self.error_messages['invalid_choice'] % value)
        return

    def get_choices_selected(self, arr_choices=''):
        if not arr_choices:
            return False
        list = []
        for choice_selected in arr_choices:
            list.append(choice_selected[0])
        return list

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^events\.models\.MultiSelectField"])


class Event(models.Model):
    """
    Model to create event templates for recurring events etc.

    :created_by: User, who owns this template.
    :creation_date: Date of the template creation.
    :title: Title of the template.
    :description: Description of the template.
    :start: Starting date of the event.
    :end: Ending date of the event.
    :venue: The event location.
    :street: Street of the event location.
    :city: City of the event location.
    :zip: ZIP code of the event location.
    :country: Country of the event location.
    :contact_person: Name of a person to contact.
    :contact_email: Email of a person to contact.
    :contact_phone: Phone of a person to contact.
    :available_seats: Amount of seats available for this event.
    :hide_available_seats: Checkfield to hide the information about available
      seats in the templates.
    :max_seats_per_guest: Maximum amount of seats per guest.
    :allow_anonymous: Checkbox to allow anonymous responses.
    :required_fields: Checkbox to select required guest fields.
    :template_name: Name can be set, if this event should be reusable.
    :is_published: Checkbox to publish/unpublish an event.

    """
    created_by = models.ForeignKey(
        'auth.User',
        verbose_name=_('Created by'),
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
    )

    title = models.CharField(
        max_length=256,
        verbose_name=_('Title'),
        help_text=_('The title will also be used for the event URL.'),
    )

    slug = models.SlugField(
        max_length=256,
        verbose_name=_('Slug'),
    )

    description = models.TextField(
        max_length=1000,
        verbose_name=_('Description'),
        blank=True, null=True,
    )

    external_link = models.URLField(
        max_length=300,
        verbose_name=_('External link'),
        null=True, blank=True,
    )

    hashtag = models.CharField(
        max_length=50,
        blank=True, 
        default=''
    )

    start = models.DateTimeField(
        default=timezone.now(),
        verbose_name=_('Start date'),
    )

    end = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=1),
        verbose_name=_('End date'),
    )

    venue = models.CharField(
        max_length=100,
        verbose_name=_('Venue'),
    )

    street = models.CharField(
        max_length=100,
        verbose_name=_('Street'),
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        verbose_name=_('City'),
        blank=True,
    )

    zip = models.CharField(
        max_length=100,
        verbose_name=_('ZIP code'),
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        verbose_name=_('Country'),
        blank=True,
    )

    contact_person = models.CharField(
        max_length=100,
        verbose_name=_('Contact name'),
        blank=True,
    )

    contact_email = models.EmailField(
        verbose_name=_('Contact email'),
        blank=True,
    )

    contact_phone = models.CharField(
        max_length=100,
        verbose_name=_('Contact phone'),
        blank=True,
    )

    available_seats = models.PositiveIntegerField(
        verbose_name=_('Available seats'),
        help_text=_(
            'Set this to a number if only a limited amount of slots are '
            ' available for this event. If you chose to display this on your'
            ' site, you can create a sense of urgency for your users to'
            ' RSVP before all slots are taken. As soon as all slots are taken,'
            ' users cannot RSVP for this event any more.'),
        blank=True, null=True,
    )

    hide_available_seats = models.BooleanField(
        default=False,
        verbose_name=_('Hide available seat information'),
        help_text=_(
            'If you set the number of available seats you can check this field'
            ' in order to hide that number from your users.'),
    )

    allow_anonymous = models.BooleanField(
        default=False,
        verbose_name=_('Allow anonymous'),
        help_text=_('Even anonymous users can rsvp, without adding any info.'),
    )

    required_fields = MultiSelectField(
        verbose_name=_('Required fields'),
        max_length=250, blank=True,
        choices=REQUIRED_FIELDS_CHOICES,
    )

    max_seats_per_guest = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_('Maximum amount of seats per guest'),
        help_text=_(
            'Set this to a number if your guests can RSVP and declare that'
            ' they are bringing some friends or family. By setting this number'
            ' You can signal to the user that he or she can only bring a'
            ' certain amount of additional guests.'),
    )

    template_name = models.CharField(
        max_length=100,
        verbose_name=_('Save as template'),
        blank=True,
        help_text=_('Save this event as a template to re-use it later.'),
    )

    is_published = models.BooleanField(
        verbose_name=_('is published'),
        default=False,
    )


    IMAGE_SETTINGS = {'size': (events_settings.EVENTS_IMAGE_SIZE,
                                 events_settings.EVENTS_IMAGE_SIZE),
                        'crop': events_settings.EVENTS_IMAGE_CROP_TYPE}

    image = ThumbnailerImageField(_('image'),
                                    blank=True,
                                    upload_to=upload_to_mugshot,
                                    resize_source=IMAGE_SETTINGS,
                                    help_text=_('An event image displayed in your event page.'),
                                    null=True,)

    def __unicode__(self):
        if self.template_name:
            return '{0} ({1})'.format(self.template_name, ugettext('Template'))
        return '{0} ({1})'.format(self.title, date(self.start))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        suspects = Event.objects.filter(slug=self.slug)
        if suspects.count() > 0 and suspects[0] != self:
            while Event.objects.filter(slug=self.slug).count() > 0:
                try:
                    number = int(self.slug[-1])
                except ValueError:
                    self.slug = self.slug + '0'
                else:
                    self.slug = self.slug[:-1] + str(number + 1)
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self, url='event_detail'):
        return reverse(url, kwargs={
            'slug': self.slug,
            'year': '{0:04d}'.format(self.start.year),
            'month': '{0:02d}'.format(self.start.month),
            'day': '{0:02d}'.format(self.start.day),
        })

    def get_update_url(self):
        return self.get_absolute_url(url='event_update')

    def get_delete_url(self):
        return self.get_absolute_url(url='event_delete')

    def get_template_url(self):
        return reverse('event_create_from_template', kwargs={
            'pk': self.pk})

    def get_free_seats(self):
        reserved = self.guests.all().aggregate(models.Sum('number_of_seats'))
        if self.available_seats:
            return self.available_seats - int(reserved.get(
                'number_of_seats__sum') or 0)
        return _('Unlimited seats available.')

    def is_bookable(self):
        if self.start < timezone.now():
            return False
        return True

    def get_image_url(self):
        """
        Returns the image of the event.        
        :return:
            ``None`` when Image is not used and no default image is supplied
            by ``EVENTS_IMAGE_DEFAULT``.
        """        
        if self.image:
            return self.image.url


class EventComment(models.Model):
    """Comments in Event."""

    user = models.ForeignKey('auth.User')
    # user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    created_on = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    class Meta:
        ordering = ['id']

    def __unicode__(self):        
        return '{0} ({1})'.format(self.comment, date(self.created_on))




class Guest(models.Model):
    """
    Model to create event templates for recurring events etc.

    :event: Event to visit.
    :user: User model of the guest.
    :name: Name of the guest.
    :email: Email of the guest.
    :phone: Phone number of the guest.
    :number_of_seats: Amount of seats to book.
    :creation_date: Date of the guest model creation.
    :is_attending: If the user is attending or not. Default: True
    :message: A response from a potential attendee.

    """
    event = models.ForeignKey(
        'events.Event',
        verbose_name=_('Event'),
        related_name='guests',
    )

    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        blank=True, null=True,
    )

    name = models.CharField(
        max_length=50,
        verbose_name=_('Name'),
        blank=True,
    )

    email = models.EmailField(
        verbose_name=_('Email'),
        blank=True,
    )

    phone = models.CharField(
        max_length=50,
        verbose_name=_('Phone'),
        blank=True,
    )

    number_of_seats = models.PositiveIntegerField(
        verbose_name=_('Number of seats'),
        blank=True, null=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
    )

    is_attending = models.BooleanField(
        verbose_name=_('Attending'),
        default=True,
    )

    message = models.TextField(
        verbose_name=_('Message'),
        max_length=4000,
        blank=True,
    )

    def __unicode__(self):
        if self.user:
            return '{0} - {1}'.format(
                self.user.get_full_name() or self.user.email, self.event)
        elif self.name or self.email:
            return '{0} - {1}'.format(self.name or self.email, self.event)
        return '{0} - {1}'.format(ugettext('anonymous'), self.event)


@receiver(post_save, sender=EventComment, dispatch_uid='email_event_owner_on_add_comment_signal')
def email_event_owner_on_add_comment(sender, instance, **kwargs):
    """Email event owner when a comment is added to event."""
    subject = '[Event] User %s commented on event "%s"'
    email_template = 'events/email/owner_notification_on_add_comment.txt'
    event = instance.event
    owner = instance.event.created_by
        
    comments_mail = EventComment.objects.order_by().filter(event=event.id).values_list('user').distinct()
    comments_mail = [comments_mail]
    user_to=[]
    
    for x in comments_mail:
        for a in x:
            user_to.append(a[0])            

    # for user_mail in comments_mail:
    #     recipients_list = user_mail.
    # event_url = reverse('event.get_absolute_url', kwargs={'slug': event.slug})
    event_url = reverse('event_detail', kwargs={
            'slug': event.slug,
            'year': '{0:04d}'.format(event.start.year),
            'month': '{0:02d}'.format(event.start.month),
            'day': '{0:02d}'.format(event.start.day),
        })
    ctx_data = {'event': event, 'owner': owner, 'user': comments_mail,
                'comment': instance.comment, 'event_url': event_url}
    # if owner.userprofile.receive_email_on_add_event_comment:
    subject = subject % (instance.user.get_full_name(),
                         instance.event.title)
    send_mail_comment(subject=subject, recipients_list=user_to,
                         email_template=email_template, data=ctx_data)
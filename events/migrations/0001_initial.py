# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import events.models
from django.utils.timezone import utc
import filer.fields.image
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('title', models.CharField(help_text='The title will also be used for the event URL.', max_length=256, verbose_name='Title')),
                ('slug', models.SlugField(max_length=256, verbose_name='Slug')),
                ('description', models.TextField(max_length=1000, null=True, verbose_name='Description', blank=True)),
                ('start', models.DateTimeField(default=datetime.datetime(2015, 11, 26, 17, 31, 15, 780312, tzinfo=utc), verbose_name='Start date')),
                ('end', models.DateTimeField(default=datetime.datetime(2015, 11, 27, 17, 31, 15, 780312, tzinfo=utc), verbose_name='End date')),
                ('venue', models.CharField(max_length=100, verbose_name='Venue')),
                ('street', models.CharField(max_length=100, verbose_name='Street', blank=True)),
                ('city', models.CharField(max_length=100, verbose_name='City', blank=True)),
                ('zip', models.CharField(max_length=100, verbose_name='ZIP code', blank=True)),
                ('country', models.CharField(max_length=100, verbose_name='Country', blank=True)),
                ('contact_person', models.CharField(max_length=100, verbose_name='Contact name', blank=True)),
                ('contact_email', models.EmailField(max_length=75, verbose_name='Contact email', blank=True)),
                ('contact_phone', models.CharField(max_length=100, verbose_name='Contact phone', blank=True)),
                ('available_seats', models.PositiveIntegerField(help_text='Set this to a number if only a limited amount of slots are  available for this event. If you chose to display this on your site, you can create a sense of urgency for your users to RSVP before all slots are taken. As soon as all slots are taken, users cannot RSVP for this event any more.', null=True, verbose_name='Available seats', blank=True)),
                ('hide_available_seats', models.BooleanField(default=False, help_text='If you set the number of available seats you can check this field in order to hide that number from your users.', verbose_name='Hide available seat information')),
                ('allow_anonymous_rsvp', models.BooleanField(default=False, help_text='Even anonymous users can rsvp, without adding any info.', verbose_name='Allow anonymous RSVP')),
                ('required_fields', events.models.MultiSelectField(blank=True, max_length=250, verbose_name='Required fields', choices=[(b'name', b'Name'), (b'email', b'Email'), (b'phone', b'Phone')])),
                ('max_seats_per_guest', models.PositiveIntegerField(help_text='Set this to a number if your guests can RSVP and declare that they are bringing some friends or family. By setting this number You can signal to the user that he or she can only bring a certain amount of additional guests.', null=True, verbose_name='Maximum amount of seats per guest', blank=True)),
                ('template_name', models.CharField(help_text='Save this event as a template to re-use it later.', max_length=100, verbose_name='Save as template', blank=True)),
                ('is_published', models.BooleanField(default=False, verbose_name='is published')),
                ('created_by', models.ForeignKey(verbose_name='Created by', to=settings.AUTH_USER_MODEL)),
                ('image', filer.fields.image.FilerImageField(related_name='rsvp_event_images', verbose_name='Image', blank=True, to='filer.Image', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='Email', blank=True)),
                ('phone', models.CharField(max_length=50, verbose_name='Phone', blank=True)),
                ('number_of_seats', models.PositiveIntegerField(null=True, verbose_name='Number of seats', blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('is_attending', models.BooleanField(default=True, verbose_name='Attending')),
                ('message', models.TextField(max_length=4000, verbose_name='Message', blank=True)),
                ('event', models.ForeignKey(related_name='guests', verbose_name='Event', to='events.Event')),
                ('user', models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

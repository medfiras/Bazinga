"""URLs for the ``events`` app."""
from django.conf.urls import *

from events.views import (
    EventCreateView,
    EventCreateFromTemplateView,
    EventDeleteView,
    EventDetailView,
    EventListView,
    EventUpdateView,
    GuestCreateView,
    GuestDeleteView,
    GuestDetailView,
    GuestUpdateView,
    StaffDashboardView,
)


urlpatterns = patterns(
    '',
    url(r'^$',
        EventListView.as_view(),
        name='event_list'),

    url(r'^create/$',
        EventCreateView.as_view(),
        name='event_create'),

    url(r'^create-from-template/(?P<pk>\d+)/$',
        EventCreateFromTemplateView.as_view(),
        name='event_create_from_template'),

    url(r'^event-staff/$',
        StaffDashboardView.as_view(),
        name='event_staff'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/'
        'delete/$',
        EventDeleteView.as_view(),
        name='event_delete'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/'
        'update/$',
        EventUpdateView.as_view(),
        name='event_update'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        EventDetailView.as_view(),
        name='event_detail'),

    url(r'^(?P<event_slug>[-\w]+)/guest/create/$',
        GuestCreateView.as_view(),
        name='guest_create'),

    url(r'^(?P<event_slug>[-\w]+)/guest/(?P<pk>\d+)/update/$',
        GuestUpdateView.as_view(),
        name='guest_update'),

    url(r'^(?P<event_slug>[-\w]+)/guest/(?P<pk>\d+)/delete/$',
        GuestDeleteView.as_view(),
        name='guest_delete'),

    url(r'^(?P<event_slug>[-\w]+)/guest/(?P<pk>\d+)/$',
        GuestDetailView.as_view(),
        name='guest_detail'),
)

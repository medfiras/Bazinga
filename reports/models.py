import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.dispatch import receiver
from django.utils.timezone import now

from south.signals import post_migrate
from bazinga.utils import *


from events.models import Event
from . import (ACTIVITY_EVENT_ATTEND, ACTIVITY_EVENT_CREATE, 
				ACTIVITY_POST_EVENT_METRICS, READONLY_ACTIVITIES, VERIFIABLE_ACTIVITIES)



VERIFY_ACTIVITY_WEEKS = 2
VERIFY_ACTION = 'Verify the activity of'


@receiver(post_migrate, dispatch_uid='report_set_groups_signal')
def report_set_groups(app, sender, signal, **kwargs):
    """Set permissions to groups."""
    if (isinstance(app, basestring) and app != 'reports'):
        return True

    perms = {'add_ngreport': ['Admin', 'Mentor'],
             'change_ngreport': ['Admin', 'Mentor'],
             'delete_ngreport': ['Admin', 'Mentor'],
             'delete_ngreportcomment': ['Admin', 'Mentor']}

    add_permissions_to_groups('reports', perms)

class GenericActiveManager(models.Manager):
    """
    Generic custom manager to fetch only the objects marked with
    an active flag.
    """
    def get_query_set(self):
        return (super(GenericActiveManager, self).get_query_set()
                .filter(active=True))

class NGReport(models.Model):
    """ Continuous Reporting Model.
    In order to be able to distinguish the old
    and the new Report models, each model associated
    with the continuous reporting system will have the
    'NG' prefix (NG - New Generation).
    """
    user = models.ForeignKey(User, related_name='ng_reports')
    report_date = models.DateField(db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    mentor = models.ForeignKey(User, null=True,
                               on_delete=models.SET_NULL,
                               related_name='ng_reports_mentored')

    is_passive = models.BooleanField(default=False)
    event = models.ForeignKey(Event, null=True, blank=True)
    link = models.URLField(max_length=500, blank=True, default='')
    link_description = models.CharField(max_length=500, blank=True, default='')
    title = models.CharField(max_length=500, blank=False, default='')
    activity_description = models.TextField(blank=True, default='')
    verified_activity = models.BooleanField('I have verified this activity',
                                            blank=True, default=False)   

    objects = models.Manager()

    def _get_url_args(self):
        args = [self.user.userprofile.display_name,
                self.report_date.year,
                utils.number2month(self.report_date.month),
                self.report_date.day,
                self.id]
        return args

    def get_absolute_url(self):
        return reverse('remo.reports.views.view_ng_report',
                       args=self._get_url_args())

    def get_absolute_edit_url(self):
        return reverse('remo.reports.views.edit_ng_report',
                       args=self._get_url_args())

    def get_absolute_delete_url(self):
        return reverse('remo.reports.views.delete_ng_report',
                       args=self._get_url_args())

    @property
    def get_report_date(self):
        return self.report_date.strftime('%d %b %Y')

    @property
    def is_future_report(self):
        if self.report_date > now().date():
            return True
        return False

    def save(self, *args, **kwargs):
        """Override save for custom functionality."""

        # Make last report notificaton date NULL on new report
        today = get_date()
        
        # User streaks functionality
        one_week = datetime.timedelta(7)
        current_start = None
        longest_start = None
        longest_end = None
                
        # Save the country if possible
        saved_report = get_object_or_none(NGReport, id=self.id)
        if (saved_report and (saved_report.latitude != self.latitude or
                              saved_report.longitude != self.longitude)):
            country = None
            try:
                country = self.location.split(',')[-1].strip()
            except IndexError:
                pass
           
            self.country = country
        super(NGReport, self).save()

        # Resolve the verified action items.
        action_item_name = u'{0} {1}'.format(VERIFY_ACTION,
                                             self.user.get_full_name())
        
        if self.is_future_report:
            return

        # If there is already a running streak and the report date
        # is within this streak, update the current streak counter.
        if (current_start and self.report_date < current_start and
            self.report_date in daterange((current_start - one_week),
                                          current_start)):
            current_start = self.report_date
        # If there isn't any current streak, and the report date
        # is within the current week, let's start the counting.
        elif (not current_start and
                self.report_date in daterange(get_date(-7), today)):
            current_start = self.report_date

        # Longest streak section
        # If longest streak already exists, let's update it.
        if longest_start and longest_end:

            # Compare the number of reports registered during
            # the current streak and the number of reports
            # during the longest streak. If current streak is bigger
            # than the previous longest streak, update the longest streak.
            longest_streak_count = NGReport.objects.filter(
                report_date__range=(longest_start, longest_end),
                user=self.user).count()
            current_streak_count = NGReport.objects.filter(
                report_date__range=(current_start, today),
                user=self.user).count()
            if current_start and current_streak_count > longest_streak_count:
                longest_start = current_start
                longest_end = today

            # This happens only when a user appends a report, dated in the
            # range of longest streak counters and it's out of the range
            # of current streak counter.
            elif self.report_date in daterange(longest_start - one_week,
                                               longest_end + one_week):
                if self.report_date < longest_start:
                    longest_start = self.report_date
                elif self.report_date > longest_end:
                    longest_end = self.report_date
        else:
            # Longest streak counters are empty, let's setup their value
            longest_start = self.report_date
            longest_end = self.report_date
        

    class Meta:
        ordering = ['-report_date', '-created_on']
        get_latest_by = 'report_date'

    def __unicode__(self):
        
        return self.title


class NGReportComment(models.Model):
    """Comments in NGReport."""
    user = models.ForeignKey(User)
    report = models.ForeignKey(NGReport)
    created_on = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def _get_url_args(self):
        args = [self.report.user.userprofile.display_name,
                self.report.report_date.year,
                utils.number2month(self.report.report_date.month),
                self.report.report_date.day,
                self.report.id,
                self.id]
        return args

    def get_absolute_delete_url(self):
        return reverse('remo.reports.views.delete_ng_report_comment',
                       args=self._get_url_args())

    class Meta:
        ordering = ['id']


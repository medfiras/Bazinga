from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
try:
    from django.forms.fields import email_re
except ImportError:
    from django.core import *
from django.template.loader import render_to_string

from celery.task import task


@task
def send_mail_comment(subject, recipients_list, sender=None,
                   message=None, email_template=None, data=None,
                   headers=None):
    """Send email from /sender/ to /recipients_list/ with /subject/ and
    /message/ as body.
    """
    # Make sure that there is either a message or a template
    if not data:
        data = {}
    # If there is no body for the email and not a template
    # to render, then do nothing.
    if not message and not email_template:
        return
    # If there is both an email body, submitted by the user,
    # and a template to render as email body, then add
    # user's input to extra_content key
    elif message and email_template:
        data.update({'extra_content': message})
    # Make sure that there is a recipient
    if not recipients_list:
        return
    if not headers:
        headers = {}
    data.update({'SITE_URL': settings.SITE_URL,
                 'FROM_EMAIL': settings.EMAIL_HOST_USER})

    # Make sure subject is one line.
    subject = subject.replace('\n', ' ')

    for recipient in recipients_list:       
        to = ''
        if User.objects.filter(pk=recipient).exists():
            user = User.objects.get(pk=recipient)
            # to = '%s <%s>' % (user.get_full_name(), user.email)
            ctx_data = {'user': user,
                        'userprofile': user.profile}
            data.update(ctx_data)
        # elif email_re.match(recipient):
            to = user.email
        else:
            return

        if email_template:
            message = render_to_string(email_template, data)

        if not sender:
            email = EmailMessage(subject=subject, body=message,
                                 from_email=settings.FROM_EMAIL,
                                 to=[to], headers=headers)
        else:
            email = EmailMessage(subject=subject, body=message,
                                 from_email=sender, to=[to], cc=[sender],
                                 headers=headers)
        email.send()
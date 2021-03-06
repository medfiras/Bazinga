from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

if "notification" in settings.INSTALLED_APPS and getattr(settings, 'PRIVATE_MESSAGES_NOTIFY', True):
    from notification import models as notification
else:
    notification = None

from private_messages.models import Message
from private_messages.fields import CommaSeparatedUserField
from private_messages import signals

class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    recipient = CommaSeparatedUserField(label=_(u"Recipient"))
    subject = forms.CharField(label=_(u"Subject"), max_length=120)
    body = forms.CharField(label=_(u"Body"),
        widget=forms.Textarea(attrs={'rows': '12', 'cols':'55'}))
    
        
    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(ComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter
    
                
    def save(self, sender, parent_msg=None):
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        message_list = []
        for r in recipients:
            msg = Message(
                sender = sender,
                recipient = r,
                subject = subject,
                body = body,
            )
            if parent_msg is not None:
                msg.parent_msg = parent_msg
                parent_msg.replied_at = timezone.now()
                parent_msg.save()
                msg.save()
                message_list.append(msg)
                signals.message_repled.send(sender=ComposeForm, message=msg, user=sender)
            else:
                msg.save()
                message_list.append(msg)
                signals.message_sent.send(sender=ComposeForm, message=msg, user=sender)

            if notification:
                if parent_msg is not None:
                    notification.send([sender], "messages_replied", {'message': msg,})
                    notification.send([r], "messages_reply_received", {'message': msg,})
                else:
                    notification.send([sender], "messages_sent", {'message': msg,})
                    notification.send([r], "messages_received", {'message': msg,})
        return message_list
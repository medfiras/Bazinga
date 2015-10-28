from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import *
from django.utils.translation import ugettext_lazy as _
from django_messages.models import *


class Todo(models.Model):
	user = models.ForeignKey(User, related_name='u')
	todo = models.CharField(max_length=50)
	flag = models.CharField(max_length=2, default='1')
	priority = models.CharField(max_length=2, default='0')
	pubtime = models.DateTimeField(auto_now_add=True)
	# assigned_to = models.ForeignKey(User, related_name='a')

	def __unicode__(self):
		return u'%d %s %s' % (self.id, self.todo, self.flag)

	class Meta:
		ordering = ['priority', 'pubtime']



# class MP_Draft(Message):
# 	"""docstring for MP_Draft"""
# 	is_draft = models.BooleanField(default=False)

# 	class Meta(Message.Meta):
# 		fields = Message.Meta.fields + ('is_draft')

# 	def __init__(self, arg):
# 		super(MP_Draft, self).__init__()
# 		self.arg = arg
	
# 	def save(self, **kwargs):
# 		if not self.id:
# 			self.sent_at = timezone.now()
# 		super(Message, self).save(**kwargs)
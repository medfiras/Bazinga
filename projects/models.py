from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import *
from django.core.validators import URLValidator

class Projects(models.Model):
	"""docstring for Projects"""
	
	uuid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100, unique=True)
	version = models.CharField(max_length=100, blank=True, null=True)
	enabled = models.BooleanField(default=True)
	description = models.TextField(blank=True, null=True)
	created_on = models.DateTimeField(default=timezone.now)
	due_date = models.DateTimeField(default=timezone.now)
	updated_on = models.DateTimeField(default=timezone.now)
	owner = models.ForeignKey(User)
	github = models.TextField(validators=[URLValidator()])
	# contributors = models.ManyToManyField(User, related_name='u+', blank=True, null=True)
	

	def __unicode__(self):
		return self.name

	def json(self):
		return{
			'uuid': self.uuid,
			'name': self.name,
			'version': self.version,
			'enabled': self.enabled,
			'description': self.description,
			'created_on': self.created_on,
			'updated_on': self.updated_on,
			'owner': self.owner,
			'github': self.github,
			'due_date': self.due_date,
		}
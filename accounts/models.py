from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from django.core.validators import URLValidator
from django.contrib import admin
#from phonenumber_field.modelfields import PhoneNumberField

class Group(models.Model):
	"""docstring for Groupe"""
	uuid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100, unique=True, blank=False, null=False)
	description = models.TextField(blank=True, null=True)
	def __unicode__(self):
		return self.name

class MyProfile(UserenaBaseProfile):
	user = models.OneToOneField(User,unique=True,verbose_name=_('user'),related_name='profile')
	group = models.ForeignKey(Group,blank=True, null=True)
	birth_date = models.DateField(blank=True, null=True)
	address = models.TextField(blank=True, null=True)
	#telephone = models.PhoneNumberField(blank=True)
	about = models.TextField(blank=True, null=True)
	city = models.CharField(max_length=100,blank=True, null=True)
	GENDER_CHOICES = (('M', 'Male'),('F', 'Female'))
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES,blank=True, null=True)
	github = models.CharField(max_length=100,validators=[URLValidator()],blank=True, null=True)
	facebook = models.CharField(max_length=100,validators=[URLValidator()],blank=True, null=True)
	twitter = models.CharField(max_length=100,validators=[URLValidator()],blank=True, null=True)
	googleplus = models.CharField(max_length=100,validators=[URLValidator()],blank=True, null=True)
	website = models.CharField(max_length=100,validators=[URLValidator()],blank=True, null=True)


class GroupAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]
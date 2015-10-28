from django.conf import settings
from django.template import RequestContext
import django_messages

def details(request):	
	return {
	'site_url': settings.SITE_URL,
	'site_name': settings.SITE_NAME,
	'site_version': settings.SITE_VERSION,
	}

# def next_message(request, message_id):
	
# 	print "==================================="
# 	print message_id
# 	print "==================================="
# 	return{'message_id':message_id}
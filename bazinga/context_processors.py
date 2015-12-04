from django.conf import settings
from django.template import RequestContext
import private_messages

def details(request):	
	return {
	'site_url': settings.SITE_URL,
	'site_name': settings.SITE_NAME,
	'site_version': settings.SITE_VERSION,
	'SITE_NAME_SHORT': settings.SITE_NAME_SHORT,
	}

# def next_message(request, message_id):
	
# 	print "==================================="
# 	print message_id
# 	print "==================================="
# 	return{'message_id':message_id}
from django.apps import AppConfig
from actstream import registry

class DjangoContribAuthConfig(AppConfig):
	name = 'django.contrib.auth'

	def ready(self):
		registry.register(self.get_model('User'))
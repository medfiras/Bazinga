from django.contrib import admin

# Register your models here.

"""Django Admin-Settings for models of the ``events`` application."""
from django.contrib import admin

from events.models import Event, Guest


class EventAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}


admin.site.register(Event, EventAdmin)
admin.site.register(Guest)

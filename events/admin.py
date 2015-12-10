from django.contrib import admin

# Register your models here.

"""Django Admin-Settings for models of the ``events`` application."""
from django.contrib import admin

from events.models import Event, Guest, EventComment


class EventAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}


class EventCommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'created_on', 'comment')

admin.site.register(Event, EventAdmin)
admin.site.register(Guest)
admin.site.register(EventComment, EventCommentAdmin)

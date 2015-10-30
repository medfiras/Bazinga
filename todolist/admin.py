from django.contrib import admin
from todolist.models import Item, List, Comment


class ItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'list', 'priority', 'due_date')
	list_filter = ('list',)
	ordering = ('priority',)
	search_fields = ('name',)


class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'date', 'body')


admin.site.register(List)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Item, ItemAdmin)
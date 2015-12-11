from django.contrib import admin

from import_export import fields, resources
from import_export.admin import ExportMixin

from .models import NGReport, NGReportComment


class NGReportCommentInline(admin.StackedInline):
    """NGReportComment Inline."""
    model = NGReportComment
    extra = 1


class NGReportResource(resources.ModelResource):
    user = fields.Field()

    class Meta:
        model = NGReport

    def dehydrate_user(self, ngreport):
        return ngreport.user.get_full_name()


class NGReportAdmin(ExportMixin, admin.ModelAdmin):
    """New Generation Report Admin."""
    resource_class = NGReportResource
    inlines = [NGReportCommentInline]

    list_display = ('user', 'title', 'report_date', 'created_on', 'updated_on', 'verified_activity')
    search_fields = ['user__first_name', 'user__last_name',
                     'user__userprofile__display_name', 'user']
    list_filter = ['report_date', 'user']

admin.site.register(NGReport, NGReportAdmin)

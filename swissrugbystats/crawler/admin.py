from django.contrib import admin
from swissrugbystats.crawler.models import CrawlerLogMessage


class CrawlerLogMessageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'message_type', 'message', 'object_type', 'object_id']
    readonly_fields = ['date', 'message_type', 'message', 'object_type', 'object_id']
    search_fields = ['message']
    list_filter = ['date', 'message_type', 'object_type']


admin.site.register(CrawlerLogMessage, CrawlerLogMessageAdmin)
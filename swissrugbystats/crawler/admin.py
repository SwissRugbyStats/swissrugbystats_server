from django.contrib import admin
from swissrugbystats.crawler.models import CrawlerLogMessage
from swissrugbystats.crawler import tasks

class CrawlerLogMessageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'message_type', 'message', 'object_type', 'object_id']
    readonly_fields = ['date', 'message_type', 'message', 'object_type', 'object_id']
    search_fields = ['message']
    list_filter = ['date', 'message_type', 'object_type']
    actions = ['crawl_and_update']

    def crawl_and_update(self, request, queryset):
        tasks.update_all()
        self.message_user(request, "Crawl started! This may take some time. Check the logs in 5-10 minutes to see if it was successful.")
    crawl_and_update.short_description = "Start Crawler"



admin.site.register(CrawlerLogMessage, CrawlerLogMessageAdmin)
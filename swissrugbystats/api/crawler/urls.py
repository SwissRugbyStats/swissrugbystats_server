from django.conf.urls import url

from swissrugbystats.api.crawler import views as crawler_views

urlpatterns = [
    url(r'^crawler/logs/?$', crawler_views.CrawlerLogMessageList.as_view(), name='crawler-logs'),
    url(r'^crawler/logs/(?P<pk>[0-9]+)/?$', crawler_views.CrawlerLogMessageDetail.as_view(), name='crawler-log-detail'),
    url(r'^crawler/start/?$', crawler_views.start, name='crawler-start')
]

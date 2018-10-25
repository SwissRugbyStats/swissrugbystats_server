from django.urls import path

from swissrugbystats.api.crawler import views as crawler_views

urlpatterns = [
    path('crawler/logs', crawler_views.CrawlerLogMessageList.as_view(), name='crawler-logs'),
    path('crawler/logs/<int:pk>', crawler_views.CrawlerLogMessageDetail.as_view(), name='crawler-log-detail'),
    path('crawler/start', crawler_views.start, name='crawler-start')
]

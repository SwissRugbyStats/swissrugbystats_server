from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from swissrugby import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^leagues/$', views.LeagueList.as_view()),
    url(r'^leagues/(?P<pk>[0-9]+)$', views.LeagueDetail.as_view()),
    url(r'^games/$', views.GameList.as_view()),
    url(r'^games/(?P<pk>[0-9]+)/$', views.GameDetail.as_view()),
    url(r'^gameparticipations/$', views.GameParticipationList.as_view()),
    url(r'^gameparticipations/(?P<pk>[0-9]+)/$', views.GameParticipationDetail.as_view()),
    url(r'^teams/$', views.TeamList.as_view()),
    url(r'^teams/(?P<pk>[0-9]+)/$', views.TeamDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
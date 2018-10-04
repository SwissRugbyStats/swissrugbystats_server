from django.conf.urls import include, url
from rest_auth.registration.views import SocialAccountListView, SocialAccountDisconnectView

from swissrugbystats.api.auth import views

urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^rest-auth/facebook/$', views.FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/twitter/$', views.TwitterLogin.as_view(), name='twitter_login'),

    # connect social media accounts
    url(r'^rest-auth/facebook/connect/$', views.FacebookConnect.as_view(), name='fb_connect'),
    url(r'^rest-auth/twitter/connect/$', views.TwitterConnect.as_view(), name='twitter_connect'),

    # list views of linked accounts
    url(r'^socialaccounts/$', SocialAccountListView.as_view(), name='social_account_list'),
    url(r'^socialaccounts/(?P<pk>\d+)/disconnect/$', SocialAccountDisconnectView.as_view(),
        name='social_account_disconnect'),

    # JWT Authentication - currently disabled
    # url(r'^api-token-auth/?', obtain_jwt_token),
    # url(r'^api-token-refresh/?', refresh_jwt_token),

]

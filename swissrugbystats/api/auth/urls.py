from django.urls import include, path
from rest_auth.registration.views import SocialAccountListView, SocialAccountDisconnectView

from swissrugbystats.api.auth import views

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('accounts/', include('allauth.urls')),

    path('rest-auth/facebook', views.FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/twitter', views.TwitterLogin.as_view(), name='twitter_login'),

    # connect social media accounts
    path('rest-auth/facebook/connect', views.FacebookConnect.as_view(), name='fb_connect'),
    path('rest-auth/twitter/connect', views.TwitterConnect.as_view(), name='twitter_connect'),

    # list views of linked accounts
    path('socialaccounts', SocialAccountListView.as_view(), name='social_account_list'),
    path('socialaccounts/<int:pk>/disconnect', SocialAccountDisconnectView.as_view(),
         name='social_account_disconnect'),

    # JWT Authentication - currently disabled
    # re_path(r'^api-token-auth/?', obtain_jwt_token),
    # re_path(r'^api-token-refresh/?', refresh_jwt_token),

]

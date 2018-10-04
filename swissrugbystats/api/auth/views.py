# -*- coding: utf-8 -*-
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.registration.views import SocialConnectView
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterConnectSerializer
from rest_auth.social_serializers import TwitterLoginSerializer


class TwitterLogin(SocialLoginView):
    """
    Allow login with Twitter.
    """
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class FacebookLogin(SocialLoginView):
    """
    Allow login with Facebook.
    """
    adapter_class = FacebookOAuth2Adapter


class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter


class TwitterConnect(SocialConnectView):
    serializer_class = TwitterConnectSerializer
    adapter_class = TwitterOAuthAdapter

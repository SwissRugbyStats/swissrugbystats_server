from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from swissrugbystats import settings

urlpatterns = [
                  # Examples:
                  # url(r'^$', 'swissrugbystats.views.home', name='home'),
                  # url(r'^blog/', include('blog.urls')),
                  url(r'^', include('swissrugbystats.api.urls')),
                  # url(r'^auth/', include('rest_framework_social_oauth2.urls')),
                  url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
                  url(r'^admin/', include(admin.site.urls)),

                  url(r'^rest-auth/', include('rest_auth.urls')),
                  url(r'^accounts/', include('allauth.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

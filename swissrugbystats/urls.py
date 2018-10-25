from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from swissrugbystats import settings

urlpatterns = [
                  # Examples:
                  # url(r'^$', 'swissrugbystats.views.home', name='home'),
                  # url(r'^blog/', include('blog.urls')),
                  path('', include('swissrugbystats.api.urls')),
                  # url(r'^auth/', include('rest_framework_social_oauth2.urls')),
                  # url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
                  path('admin', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

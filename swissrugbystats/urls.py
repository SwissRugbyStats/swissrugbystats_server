from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from swissrugbystats import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'swissrugbystats.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('swissrugbystats.api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True })
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
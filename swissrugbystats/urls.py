from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf.urls.static import static
from swissrugbystats import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'swissrugbystats.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('swissrugbystats.api.urls')),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^admin/', include(admin.site.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
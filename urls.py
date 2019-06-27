from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
import django.views.static


admin.autodiscover()

urlpatterns = [
    url(r'', include('lfs.core.urls')),
    url(r'^manage/', include('lfs.manage.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^paypal/ipn/', include('paypal.standard.ipn.urls')),
    url(r'^reviews/', include('reviews.urls')),
    # url(r'^io/', include('lfs_io.urls')),
    # url(r'^bulk-prices/', include("lfs_bulk_prices.urls")),
    # url(r'^samples/', include("lfs_samples.urls")),
    # url(r'^canonical/', include("lfs_canonical.urls")),
    url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
]

try:
    from local_urls import *
except ImportError:
    pass

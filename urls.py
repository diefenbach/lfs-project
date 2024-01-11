from django.urls import include, re_path
from django.conf import settings
from django.contrib import admin
import django.views.static

# from lfs_carousel.views import carousel

admin.autodiscover()

urlpatterns = [
    re_path(r"", include("lfs.core.urls")),
    re_path(r"^manage/", include("lfs.manage.urls")),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^paypal/ipn/", include("paypal.standard.ipn.urls")),
    re_path(r"^reviews/", include("reviews.urls")),
    # re_path(r'^io/', include('lfs_io.urls')),
    # re_path(r'^bulk-prices/', include("lfs_bulk_prices.urls")),
    # re_path(r'^samples/', include("lfs_samples.urls")),
    # re_path(r'^canonical/', include("lfs_canonical.urls")),
    re_path(r"^media/(?P<path>.*)$", django.views.static.serve, {"document_root": settings.MEDIA_ROOT}),
    # re_path(r'^carousel/', include(carousel.urls)),
]

try:
    from local_urls import *
except ImportError:
    pass

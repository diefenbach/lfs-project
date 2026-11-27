"""URLs of the shop: the storefront, the management interface, and the add-ons."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("lfs.core.urls")),
    path("manage/", include("lfs.manage.urls")),
    path("admin/", admin.site.urls),
    path("reviews/", include("reviews.urls")),
    path("captcha/", include("captcha.urls")),
    path("canonical/", include("lfs_canonical.urls")),
    # The theme loads the mobile menu from here instead of putting it into every page.
    path("theme/", include("lfs_theme.urls")),
]

if "lfs_bulk_prices" in settings.INSTALLED_APPS:
    urlpatterns.append(path("bulk-prices/", include("lfs_bulk_prices.urls")))

if "lfs_paypal" in settings.INSTALLED_APPS:
    urlpatterns.append(path("paypal/", include("lfs_paypal.urls")))

if "lfs_stripe" in settings.INSTALLED_APPS:
    urlpatterns.append(path("stripe/", include("lfs_stripe.urls")))

if settings.DEBUG:
    # In production the web server serves uploaded files.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

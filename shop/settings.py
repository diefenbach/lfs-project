"""Settings of the shop.

Everything that differs between installations comes from environment variables (see ``.env.example``); the rest
configures LFS and its add-ons. Without ``POSTGRES_DB`` the shop uses SQLite in ``db.sqlite3``.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name: str, default: bool = False) -> bool:
    """Return the environment variable ``name`` as a boolean ("1", "true", "yes", "on" are true)."""
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


def env_list(name: str, default: str = "") -> list[str]:
    """Return the comma-separated environment variable ``name`` as a list without empty items."""
    return [item.strip() for item in os.environ.get(name, default).split(",") if item.strip()]


# Django

DEBUG = env_bool("DJANGO_DEBUG")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured("Set DJANGO_SECRET_KEY (or DJANGO_DEBUG=true for local development).")
    SECRET_KEY = "django-insecure-local-development-only"

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

if os.environ.get("POSTGRES_DB"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["POSTGRES_DB"],
            "USER": os.environ.get("POSTGRES_USER", ""),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

INSTALLED_APPS = [
    # The theme comes first, so its templates win over those of LFS and the add-ons.
    "lfs_theme",
    "crispy_forms",
    "crispy_bootstrap5",
    "compressor",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.redirects",
    "django.contrib.sitemaps",
    "django_countries",
    "localflavor",
    "captcha",
    # LFS and the add-ons it needs
    "reviews",
    "portlets",
    "postal",
    "lfs.addresses",
    "lfs.caching",
    "lfs.cart",
    "lfs.catalog",
    "lfs.checkout",
    "lfs.core",
    "lfs.criteria",
    "lfs.customer",
    "lfs.customer_tax",
    "lfs.discounts",
    "lfs.export",
    "lfs.gross_price",
    "lfs.mail",
    "lfs.manage",
    "lfs.marketing",
    "lfs.manufacturer",
    "lfs.net_price",
    "lfs.order",
    "lfs.page",
    "lfs.payment",
    "lfs.portlet",
    "lfs.search",
    "lfs.shipping",
    "lfs.supplier",
    "lfs.tax",
    "lfs.utils",
    "lfs.voucher",
    "lfs_contact",
    "lfs_order_numbers",
    "lfs_paypal",
    # Standard add-ons
    "lfs_canonical",
    "lfs_cookie_consent",
    # Optional: "lfs_stripe" (install lfs-project[stripe]), "lfs_carousel", "lfs_bulk_prices", "lfs_samples", ...
]
if os.environ.get("POSTGRES_DB"):
    # PostgreSQL's unaccent: the search then ignores accents (creme finds crème).
    INSTALLED_APPS.append("django.contrib.postgres")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "shop.urls"
WSGI_APPLICATION = "shop.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "lfs.core.context_processors.main",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = ["lfs.customer.auth.EmailBackend", "django.contrib.auth.backends.ModelBackend"]
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/manage/"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = os.environ.get("DJANGO_LANGUAGE_CODE", "en")
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "Europe/Berlin")
USE_I18N = True
USE_TZ = True

SITE_ID = 1
SESSION_SERIALIZER = "lfs.core.pickle_serializer.PickleSerializer"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
COMPRESS_ENABLED = False

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

# E-mail: printed to the console in development, sent via SMTP otherwise.
if DEBUG and not os.environ.get("EMAIL_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "webmaster@localhost")

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    if env_bool("DJANGO_BEHIND_PROXY"):
        # Behind a reverse proxy that terminates HTTPS and sets X-Forwarded-Proto.
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Errors reach the console (and thus the server's log) with their traceback.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}

# Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# LFS
LFS_CURRENCY = os.environ.get("LFS_CURRENCY", "EUR")
LFS_DOCS = "https://github.com/diefenbach/django-lfs"
LFS_AFTER_ADD_TO_CART = "lfs_added_to_cart"
LFS_RECENT_PRODUCTS_LIMIT = 5
LFS_ORDER_NUMBER_GENERATOR = "lfs_order_numbers.models.OrderNumberGenerator"

LFS_INVOICE_COMPANY_NAME_REQUIRED = False
LFS_INVOICE_EMAIL_REQUIRED = True
LFS_INVOICE_PHONE_REQUIRED = True
LFS_SHIPPING_COMPANY_NAME_REQUIRED = False
LFS_SHIPPING_EMAIL_REQUIRED = False
LFS_SHIPPING_PHONE_REQUIRED = False

LFS_PAYMENT_METHOD_PROCESSORS = [
    ["lfs_paypal.processor.PayPalProcessor", _("PayPal")],
]
LFS_PRICE_CALCULATORS = [
    ["lfs.gross_price.calculator.GrossPriceCalculator", _("Price includes tax")],
    ["lfs.net_price.calculator.NetPriceCalculator", _("Price excludes tax")],
]
LFS_SHIPPING_METHOD_PRICE_CALCULATORS = [
    ["lfs.shipping.calculator.GrossShippingMethodPriceCalculator", _("Price includes tax")],
    ["lfs.shipping.calculator.NetShippingMethodPriceCalculator", _("Price excludes tax")],
]
LFS_UNITS = ["l", "m", "qm", "cm", "lfm", "kg", "pcs."]
LFS_PRICE_UNITS = LFS_BASE_PRICE_UNITS = LFS_PACKING_UNITS = LFS_UNITS
LFS_CRITERIA = [
    ["lfs.criteria.models.CartPriceCriterion", _("Cart Price")],
    ["lfs.criteria.models.CombinedLengthAndGirthCriterion", _("Combined Length and Girth")],
    ["lfs.criteria.models.CountryCriterion", _("Country")],
    ["lfs.criteria.models.HeightCriterion", _("Height")],
    ["lfs.criteria.models.LengthCriterion", _("Length")],
    ["lfs.criteria.models.WidthCriterion", _("Width")],
    ["lfs.criteria.models.WeightCriterion", _("Weight")],
    ["lfs.criteria.models.ShippingMethodCriterion", _("Shipping Method")],
    ["lfs.criteria.models.PaymentMethodCriterion", _("Payment Method")],
]

# PayPal (lfs-paypal): sandbox until you set your live credentials.
PAYPAL_MODE = os.environ.get("PAYPAL_MODE", "sandbox")
PAYPAL_CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID", "")
PAYPAL_CLIENT_SECRET = os.environ.get("PAYPAL_CLIENT_SECRET", "")

# Stripe (lfs-stripe, optional)
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_SHOP_NAME = os.environ.get("STRIPE_SHOP_NAME", "LFS")

# Reviews (django-reviews)
REVIEWS_SHOW_PREVIEW = False
REVIEWS_IS_NAME_REQUIRED = False
REVIEWS_IS_EMAIL_REQUIRED = False
REVIEWS_IS_MODERATED = False

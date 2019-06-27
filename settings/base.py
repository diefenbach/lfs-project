# coding=utf-8

import os
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!yxfrws8+^v2b!m4)v4m&8^xytn0&l%sm__9o6^-7(3v9h0)t+'


INSTALLED_APPS = (
    'lfs_theme',
    'compressor',
    "django.contrib.admin",
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'django.contrib.sitemaps',
    'django_countries',
    'reviews',
    'portlets',
    'lfs.addresses',
    'lfs.caching',
    'lfs.cart',
    'lfs.catalog',
    'lfs.checkout',
    'lfs.core',
    'lfs.criteria',
    'lfs.customer',
    'lfs.customer_tax',
    'lfs.discounts',
    'lfs.export',
    'lfs.gross_price',
    'lfs.mail',
    'lfs.manage',
    'lfs.marketing',
    'lfs.manufacturer',
    'lfs.net_price',
    'lfs.order',
    'lfs.page',
    'lfs.payment',
    'lfs.portlet',
    'lfs.search',
    'lfs.shipping',
    'lfs.supplier',
    'lfs.tax',
    'lfs.tests',
    'lfs.utils',
    'lfs.voucher',
    'lfs_contact',
    'lfs_order_numbers',
    'localflavor',
    'postal',
    'paypal.standard.ipn',
    'lfs_paypal',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'


# WSGI_APPLICATION = 'project.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'hin',
    },
}


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                        # Or path to database file if using sqlite3.
        'USER': '',                              # Not used with sqlite3.
        'PASSWORD': '',                          # Not used with sqlite3.
        'HOST': '',                              # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                              # Set to empty string for default. Not used with sqlite3.
    }
}

AUTHENTICATION_BACKENDS = (
    'lfs.customer.auth.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/manage/"

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR + "/media"

SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"
SITE_ID = 1

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + "/sitestatic"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'lfs.core.context_processors.main',
            ],
        },
    },
]

# LFS
# see http://docs.getlfs.com/en/latest/developer/settings.html for more

PAYPAL_RECEIVER_EMAIL = "info@yourbusiness.com"
PAYPAL_IDENTITY_TOKEN = "set_this_to_your_paypal_pdt_identity_token"

LFS_PAYPAL_REDIRECT = True
LFS_AFTER_ADD_TO_CART = "lfs_added_to_cart"
LFS_RECENT_PRODUCTS_LIMIT = 5

LFS_LOCALE = "de_DE.UTF-8"

LFS_ORDER_NUMBER_GENERATOR = "lfs_order_numbers.models.OrderNumberGenerator"
LFS_DOCS = "http://docs.getlfs.com/en/latest/"

LFS_INVOICE_COMPANY_NAME_REQUIRED = False
LFS_INVOICE_EMAIL_REQUIRED = True
LFS_INVOICE_PHONE_REQUIRED = True

LFS_SHIPPING_COMPANY_NAME_REQUIRED = False
LFS_SHIPPING_EMAIL_REQUIRED = False
LFS_SHIPPING_PHONE_REQUIRED = False

LFS_PAYMENT_METHOD_PROCESSORS = [
    ["lfs_paypal.processor.PayPalProcessor", _(u"PayPal")],
    ["lfs_sofortueberweisung.models.SofortUeberweisungPaymentMethodProcessor", "sofortueberweisung.de"],
    ["lfs_paymill.models.PaymillPaymentMethodProcessor", "Paymill"],
]

LFS_PRICE_CALCULATORS = [
    ['lfs.gross_price.calculator.GrossPriceCalculator', _(u'Price includes tax')],
    ['lfs.net_price.calculator.NetPriceCalculator', _(u'Price excludes tax')],
    ["lfs_bulk_prices.calculator.BulkPricesCalculator", _(u"Bulk prices calculator")],
]

LFS_SHIPPING_METHOD_PRICE_CALCULATORS = [
    ["lfs.shipping.calculator.GrossShippingMethodPriceCalculator", _(u'Price includes tax')],
    ["lfs.shipping.calculator.NetShippingMethodPriceCalculator", _(u'Price excludes tax')],
    ["hin_shipping_calculator.calculator.HINShippingMethodPriceCalculator", "HIN"],
]

LFS_UNITS = [
    u"l",
    u"m",
    u"qm",
    u"cm",
    u"lfm",
    u"Paket(e)",
    u"Stück",
]

LFS_PRICE_UNITS = LFS_BASE_PRICE_UNITS = LFS_PACKING_UNITS = LFS_UNITS

LFS_CRITERIA = [
    ["lfs.criteria.models.CartPriceCriterion", _(u"Cart Price")],
    ["lfs.criteria.models.CombinedLengthAndGirthCriterion", _(u"Combined Length and Girth")],
    ["lfs.criteria.models.CountryCriterion", _(u"Country")],
    ["lfs.criteria.models.HeightCriterion", _(u"Height")],
    ["lfs.criteria.models.LengthCriterion", _(u"Length")],
    ["lfs.criteria.models.WidthCriterion", _(u"Width")],
    ["lfs.criteria.models.WeightCriterion", _(u"Weight")],
    ["lfs.criteria.models.ShippingMethodCriterion", _(u"Shipping Method")],
    ["lfs.criteria.models.PaymentMethodCriterion", _(u"Payment Method")],
    ["lfs_criterion_us_states.models.USStatesCriterion", _(u"US State")],
]


REVIEWS_SHOW_PREVIEW = False
REVIEWS_IS_NAME_REQUIRED = False
REVIEWS_IS_EMAIL_REQUIRED = False
REVIEWS_IS_MODERATED = False

LFS_ONE_PAGE_CHECKOUT_FORM = "holzimgarten_app.forms.HigOnePageCheckoutForm"
LFS_CONTACT_FORM = "hin_theme.ContactForm"

LFS_SITEMAPS = {
    "product": {
        "sitemap": "holzimgarten_app.sitemaps.ProductSitemap",
    },
    "category": {
        "protocol": "https",
    },
    "page": {
        "protocol": "https",
    },
    "shop": {
        "protocol": "https",
    },
}

PRODUCT_TEMPLATES = (
    (0, {"file": "%s/%s" % ("lfs/catalog/products", "product_inline.html"),
        "image": "/media/lfs/icons" + "/product_default.png",
        "name": _(u"Default")
    },),
    (1, {"file": "%s/%s" % ("lfs/catalog/products", "product_offer_inline.html"),
        "image": "/media/lfs/icons" + "/product_default.png",
        "name": _(u"Mengenrabatt")
    },),
    (2, {"file": "%s/%s" % ("lfs/catalog/products", "product_example_inline.html"),
        "image": "/media/lfs/icons" + "/product_example.png",
        "name": _(u"Muster")
    },),
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%a, %d %b %Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, "lfs.log"),
            'mode': 'a',
        },
    },
    "loggers": {
        "django": {
            "handlers": ["logfile", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "lfs": {
            "handlers": ["logfile"],
            "level": "DEBUG",
            "propagate": False,
        },
        "lfs_io": {
            "handlers": ["logfile"],
            "level": "DEBUG",
            "propagate": False,
        },
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--nocapture', '--verbosity=1']

# apps that we want jenkins ci to test
PROJECT_APPS = ['lfs.core']
JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    #'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    #'django_jenkins.tasks.windmill_tests',
)

PISTON_DISPLAY_ERRORS = True

COMPRESS_ENALBED = True
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSCompressorFilter',
]

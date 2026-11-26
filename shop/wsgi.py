"""WSGI entry point for production servers such as gunicorn (``gunicorn shop.wsgi``)."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")

application = get_wsgi_application()

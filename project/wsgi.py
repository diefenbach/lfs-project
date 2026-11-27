"""WSGI entry point for production servers such as gunicorn (``gunicorn project.wsgi``)."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = get_wsgi_application()

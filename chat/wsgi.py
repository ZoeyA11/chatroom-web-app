"""
WSGI config for chat project.
It exposes the WSGI callable as a module-level variable named ``application``.
Django's primary deployment platform is WSGI, the Python standard for web servers and applications.
A built-in Django server, ie the runserver command, reads it from the WSGI_APPLICATION definition.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat.settings")

application = get_wsgi_application()

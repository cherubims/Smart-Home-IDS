"""
WSGI config for smarthome_network_ids project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smarthome_network_ids.settings')

application = get_wsgi_application()

# api/settings.py
WSGI_APPLICATION = 'smarthome_network_ids.wsgi.application'

"""
WSGI config for verifier project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from views import VerifierWebsite
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "verifier.settings")
application = get_wsgi_application()
# Configuration file directory is read from settings:
config_dir = settings.CONFIG_DIR
# Verifier thread is started:
VerifierWebsite(config_dir).start_web_verifier()

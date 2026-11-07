"""
WSGI config for the PyCon Portugal 2027 website.

It exposes the WSGI callable as a module-level variable named ``application``,
used by gunicorn in production and by Django's ``runserver``.
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# This allows easy placement of apps within the interior
# pycon_portugal_2027 directory.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "pycon_portugal_2027"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

application = get_wsgi_application()

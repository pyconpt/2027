"""
Base settings for the PyCon Portugal 2027 website.

The site is a static content site rendered from Markdown files: there is no
database, no authentication and no user generated content.
"""

from pathlib import Path

import environ
from django.utils.csp import CSP

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# pycon_portugal_2027/
APPS_DIR = BASE_DIR / "pycon_portugal_2027"
# Markdown pages live here, one folder per menu/submenu.
CONTENT_DIR = APPS_DIR / "content"

env = environ.Env()
if env.bool("DJANGO_READ_DOT_ENV_FILE", default=True):
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", False)
TIME_ZONE = "Europe/Lisbon"
LANGUAGE_CODE = "en-us"
USE_I18N = False
USE_TZ = True

# No database: all content comes from Markdown files.
DATABASES: dict = {}

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "pycon_portugal_2027.site",
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware",
    "pycon_portugal_2027.site.middleware.PermissionsPolicyMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
]

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.csp",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "pycon_portugal_2027.site.context_processors.links",
            ],
        },
    },
]

# SECURITY
# ------------------------------------------------------------------------------
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

# Third parties the pages use: Google Analytics (only after cookie consent, see
# project.js), the pretalx schedule widget and the Google Maps embed
# on the venue page. Inline <script>s need {{ csp_nonce }}. Inline styles stay
# allowed: Markdown content and the pretalx widget use them, and without inline
# scripts they can't be used to run code.
GOOGLE_ANALYTICS = ["https://*.google-analytics.com", "https://*.analytics.google.com", "https://*.googletagmanager.com"]
PRETALX = "https://pretalx.evolutio.pt"
SECURE_CSP = {
    "default-src": [CSP.SELF],
    "script-src": [CSP.SELF, CSP.NONCE, "https://www.googletagmanager.com", PRETALX],
    "style-src": [CSP.SELF, CSP.UNSAFE_INLINE],
    # Self-hosted, see static/fonts/
    "font-src": [CSP.SELF],
    "img-src": [CSP.SELF, "data:", PRETALX, *GOOGLE_ANALYTICS],
    "connect-src": [CSP.SELF, PRETALX, *GOOGLE_ANALYTICS],
    "frame-src": ["https://www.google.com"],
    "frame-ancestors": [CSP.NONE],
    "object-src": [CSP.NONE],
    "base-uri": [CSP.SELF],
    "form-action": [CSP.SELF],
}

# Powerful browser features the site never uses (Django has no setting for this
# header, see pycon_portugal_2027.site.middleware).
PERMISSIONS_POLICY = {
    "accelerometer": [],
    "camera": [],
    "display-capture": [],
    "geolocation": [],
    "gyroscope": [],
    "magnetometer": [],
    "microphone": [],
    "payment": [],
    "usb": [],
}

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

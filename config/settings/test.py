"""
With these settings, tests run faster.
"""

from .base import *  # noqa: F403
from .base import TEMPLATES
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="gmAJ39B8qNh9BwUX7XidFvFpeCQTTqosh53WmEEviGGrOxHteiGgypIBIk0Jk0rQ",
)
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# WhiteNoise: serve from the finders, no collected staticfiles/ directory needed
# ------------------------------------------------------------------------------
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# DEBUGGING FOR TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore[index]

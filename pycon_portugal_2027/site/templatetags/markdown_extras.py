import re
from pathlib import Path

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.templatetags.static import static
from markdown import Markdown

register = template.Library()

# src="...", href="..." and srcset="..." attributes of the rendered HTML
_URL_ATTRIBUTE_RE = re.compile(r'\b(src|href|srcset)="([^"]*)"')


def _static_url(match):
    """Swap a hard-coded ``/static/<path>`` for ``static(path)``."""
    path = match.group(1)
    try:
        return static(path)
    except ValueError:
        # not in the manifest (a typo, or collectstatic wasn't run): keep the plain URL
        return match.group(0)


def _versioned_static_urls(html):
    """Point the ``/static/`` URLs written in Markdown at the hashed files of the manifest storage.

    Templates get those through ``{% static %}``; without this, content images are served
    under their plain name, which WhiteNoise can't cache for long.
    """
    # only at the start of a URL: the attribute's start, or after a srcset separator
    static_path_re = re.compile(r"(?<![^\s,])" + re.escape(settings.STATIC_URL) + r"([^\s,\"]+)")

    def attribute(match):
        name, value = match.groups()
        return f'{name}="{static_path_re.sub(_static_url, value)}"'

    return _URL_ATTRIBUTE_RE.sub(attribute, html)


@register.filter()
@stringfilter
def markdown(value):
    """Render the Markdown file at ``value`` and return its HTML and front-matter."""
    md = Markdown(extensions=["extra", "nl2br", "sane_lists", "meta", "toc"])
    html = md.convert(Path(value).read_text(encoding="utf-8"))
    return {"html": _versioned_static_urls(html), "meta": md.Meta}

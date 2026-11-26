import re
from pathlib import Path

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from markdown import Markdown

register = template.Library()

# a paragraph that is only "[[name]]": a widget, rendered from templates/modules/widgets/<name>.html
_WIDGET_RE = re.compile(r"<p>\[\[([a-z_]+)\]\]</p>")

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


@register.simple_tag(takes_context=True)
def render_content(context, html):
    """Return the rendered Markdown ``html`` with its ``[[name]]`` widgets filled in.

    Markdown is static, so the parts that change with the site's state (the CFP
    button follows ``cfp_open``) are templates rendered with the page's context.
    """

    def widget(match):
        return context.template.engine.get_template(f"modules/widgets/{match.group(1)}.html").render(context)

    return mark_safe(_WIDGET_RE.sub(widget, html))  # noqa: S308 - our own Markdown and templates

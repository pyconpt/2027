import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Same escaping as Django's json_script, so the JSON can't close the <script> tag
_JSON_ESCAPES = {ord("<"): "\\u003C", ord(">"): "\\u003E", ord("&"): "\\u0026"}


@register.filter()
def jsonld(value):
    """Render ``value`` as a ``<script type="application/ld+json">`` block."""
    data = json.dumps(value, ensure_ascii=False, separators=(",", ":")).translate(_JSON_ESCAPES)
    return mark_safe(f'<script type="application/ld+json">{data}</script>')  # noqa: S308

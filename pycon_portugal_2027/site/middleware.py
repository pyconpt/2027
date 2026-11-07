from django.conf import settings


class PermissionsPolicyMiddleware:
    """Send the ``Permissions-Policy`` header built from ``settings.PERMISSIONS_POLICY``.

    Each feature maps to its allowlist, e.g. ``{"camera": []}`` gives ``camera=()``
    (disabled everywhere) and ``{"fullscreen": ["self"]}`` gives ``fullscreen=(self)``.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.header = ", ".join(
            f"{feature}=({' '.join(allowlist)})" for feature, allowlist in settings.PERMISSIONS_POLICY.items()
        )

    def __call__(self, request):
        response = self.get_response(request)
        response.headers.setdefault("Permissions-Policy", self.header)
        return response

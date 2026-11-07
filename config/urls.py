from django.conf import settings
from django.templatetags.static import static
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import RedirectView

from pycon_portugal_2027.site.views import default_view
from pycon_portugal_2027.site.views import robots_txt
from pycon_portugal_2027.site.views import sitemap_xml


class FaviconView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return static("images/logo/logo-pycon2027.svg")


urlpatterns = [
    path("", default_view, name="home"),
    path("favicon.ico", FaviconView.as_view()),
    path("robots.txt", robots_txt, name="robots"),
    path("sitemap.xml", sitemap_xml, name="sitemap"),
    path("<slug:menu>/", default_view, name="menu-view"),
    path("<slug:menu>/<slug:submenu>/", default_view, name="submenu-view"),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]

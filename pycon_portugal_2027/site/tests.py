import json
import re

import pytest
from django.conf import settings

from pycon_portugal_2027.site.context_processors import SITE_MENU
from pycon_portugal_2027.site.templatetags import markdown_extras
from pycon_portugal_2027.site.views import front_matter


def menu_urls():
    for entry in SITE_MENU.values():
        if isinstance(entry, dict):
            yield from entry.values()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"PyCon Portugal 2027" in response.content


@pytest.mark.parametrize("url", sorted(menu_urls()))
def test_menu_pages_render(client, url):
    assert client.get(url).status_code == 200


def test_missing_trailing_slash_redirects(client):
    assert client.get("/talks/cfp").status_code == 301


def test_unknown_page_is_404(client):
    assert client.get("/nope/").status_code == 404
    assert client.get("/talks/nope/").status_code == 404


def test_favicon_redirects_to_logo(client):
    response = client.get("/favicon.ico")
    assert response.status_code == 301
    assert response["Location"].endswith("logo-pycon2027.svg")


def sitemap_urls(client):
    sitemap = client.get("/sitemap.xml").content.decode()
    return [url.removeprefix("https://2027.pycon.pt") for url in re.findall(r"<loc>(.*?)</loc>", sitemap)]


def structured_data(response):
    script = re.search(r'<script type="application/ld\+json">(.*?)</script>', response.content.decode(), re.DOTALL)
    return {node["@type"]: node for node in json.loads(script.group(1))["@graph"]}


def test_sitemap_lists_every_content_page(client):
    urls = sitemap_urls(client)
    assert "/" in urls
    assert "/tickets/" in urls
    assert set(menu_urls()) <= set(urls)
    for url in urls:
        assert client.get(url).status_code == 200, url


def test_robots_points_to_sitemap(client):
    response = client.get("/robots.txt")
    assert response["Content-Type"].startswith("text/plain")
    assert b"Sitemap: https://2027.pycon.pt/sitemap.xml" in response.content


@pytest.mark.parametrize("url", ["/talks/cfp/", "/information/", "/tickets/", "/sponsors/sponsorship/"])
def test_pages_have_their_own_description(client, url):
    home = client.get("/").content.decode()
    page = client.get(url).content.decode()
    description = re.search(r'<meta name="description" content="(.*?)">', page).group(1)
    assert description
    assert description not in home
    assert f'<meta property="og:description" content="{description}">' in page


def test_every_content_page_has_a_description():
    # the description is read from the first Markdown file of each page
    for directory in settings.CONTENT_DIR.glob("**/"):
        files = sorted(directory.glob("*.md"))
        if files:
            assert front_matter(files[0]).get("description"), files[0]


def test_home_structured_data_has_the_event(client):
    nodes = structured_data(client.get("/"))
    assert {"Organization", "WebSite", "Event"} <= set(nodes)
    assert nodes["Event"]["startDate"] == "2027-04-22"
    assert len(nodes["Event"]["offers"]) == 3


def test_markdown_static_urls_go_through_static(monkeypatch):
    def fake_static(path):
        if path == "images/missing.png":
            raise ValueError(path)
        return f"/static/{path.replace('.', '.abc123.')}"

    monkeypatch.setattr(markdown_extras, "static", fake_static)
    html = (
        '<img src="/static/images/a.webp" srcset="/static/images/a-800.webp 800w, /static/images/a.webp 1200w">'
        '<a href="https://example.com/static/x.png">x</a><img src="/static/images/missing.png">'
        "<p>Files live in /static/images/a.webp</p>"
    )
    assert markdown_extras._versioned_static_urls(html) == (  # noqa: SLF001
        '<img src="/static/images/a.abc123.webp"'
        ' srcset="/static/images/a-800.abc123.webp 800w, /static/images/a.abc123.webp 1200w">'
        '<a href="https://example.com/static/x.png">x</a><img src="/static/images/missing.png">'
        "<p>Files live in /static/images/a.webp</p>"
    )


def test_page_structured_data_has_breadcrumbs(client):
    nodes = structured_data(client.get("/talks/cfp/"))
    items = nodes["BreadcrumbList"]["itemListElement"]
    assert [item["name"] for item in items] == ["Home", "Call for Participation"]
    assert items[-1]["item"] == "https://2027.pycon.pt/talks/cfp/"

from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from markdown import Markdown

from pycon_portugal_2027.site import structured_data
from pycon_portugal_2027.site.context_processors import PAGE_TITLES


def front_matter(file):
    """Return the front-matter of the Markdown ``file`` as ``{key: "value"}``."""
    md = Markdown(extensions=["meta"])
    md.convert(Path(file).read_text(encoding="utf-8"))
    # the meta extension gives a list of lines per key, so a value can span several lines
    return {key: " ".join(lines) for key, lines in md.Meta.items()}


def default_view(request, menu="home", submenu=None):
    """Render the home page, or every Markdown file of ``content/<menu>/<submenu>/``."""
    if menu == "home" and submenu is None:
        return render(
            request,
            "pages/home.html",
            {"menu": "Home", "structured_data": structured_data.graph(structured_data.event())},
        )

    # ``menu`` and ``submenu`` are slugs (see config/urls.py), so they can't
    # escape the content directory.
    path = settings.CONTENT_DIR / menu
    if submenu:
        path /= submenu
    if not path.is_dir():
        raise Http404

    files = sorted(str(f) for f in path.glob("*.md"))
    if not files:
        raise Http404

    title = PAGE_TITLES.get(request.path) or (submenu or menu).replace("_", " ").replace("-", " ").capitalize()
    # the page's description lives in the front-matter of its first file
    return render(
        request,
        "pages/default.html",
        {
            "menu": title,
            "files": files,
            "description": front_matter(files[0]).get("description"),
            "structured_data": structured_data.graph(structured_data.breadcrumbs(title, request.path)),
        },
    )


def robots_txt(request):
    return render(request, "robots.txt", content_type="text/plain")


def sitemap_xml(request):
    """List every content directory that has Markdown files, as default_view serves them."""
    content = settings.CONTENT_DIR
    pages = sorted(f"/{d.relative_to(content).as_posix()}/" for d in content.glob("**/") if any(d.glob("*.md")))
    return render(request, "sitemap.xml", {"pages": pages}, content_type="application/xml")

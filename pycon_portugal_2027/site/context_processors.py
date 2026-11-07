"""Site wide links: navigation menu, event services and social media."""

EVENT = {
    "name": "PyCon Portugal 2027",
    "url": "https://2027.pycon.pt",
    "description": (
        "PyCon Portugal 2027, 22–24 April 2027 in Leiria: three days of talks, workshops "  # noqa: RUF001
        "and community for Python beginners and professionals from everywhere."
    ),
    "edition": "6th",
    "dates": "22–24 April 2027",  # noqa: RUF001
    "city": "Leiria, Portugal",
    "email": "2027@pycon.pt",
    "tickets": "https://pretix.evolutio.pt/evolutio/pyconpt2027/",
    "cfp": "https://pretalx.evolutio.pt/pycon-portugal-2027/cfp",
    "pretalx": "https://pretalx.evolutio.pt/pycon-portugal-2027/",
    "github": "https://github.com/pyconpt/2027",
}

SITE_MENU = {
    "Talks": {
        "Call for Participation": "/talks/cfp/",
        "Selection Process": "/talks/selection_process/",
        "Schedule": "/talks/schedule/",
    },
    "Information": {
        "Leiria": "/information/leiria/",
        "Venue": "/information/venue/",
        "Grants": "/information/grants/",
        "Hospitality": "/information/hospitality/",
        "Party": "/information/party/",
        "T-shirts": "/information/t-shirts/",
        "FAQs": "/information/faqs/",
    },
    "Sponsors": {
        "Sponsors": "/sponsors/sponsors/",
        "Sponsorship": "/sponsors/sponsorship/",
        "Jobs": "/sponsors/jobs/",
    },
    "Conduct": {
        "Code of Conduct": "/conduct/code_of_conduct/",
        "Response Guide": "/conduct/response_guide/",
        "Privacy Guide": "/conduct/privacy_guide/",
    },
    "Tickets": EVENT["tickets"],
    "About": {
        "Contact": "/about/contact/",
        "Credits": "/about/credits/",
    },
}

# Page titles for the content pages, keyed by path: "/talks/cfp/" -> "Call for Participation"
PAGE_TITLES = {
    href: label
    for entry in SITE_MENU.values()
    if isinstance(entry, dict)
    for label, href in entry.items()
}

SOCIAL_MEDIA = {
    "x": "https://x.com/PyConPT",
    "slack": "https://join.slack.com/t/pyconportugal/shared_invite/zt-1ckszg1ye-QDgxx3lOkC15Ocal8xhCSg",
    "youtube": "https://www.youtube.com/@pyconportugal",
    "linkedin": "https://www.linkedin.com/company/84778227",
    "github": "https://github.com/pyconpt/",
}


def links(request):
    return {
        "event": EVENT,
        "site_menu": SITE_MENU,
        "social_media": SOCIAL_MEDIA,
    }

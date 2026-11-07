"""schema.org JSON-LD for search engines: the organization, the website, the event and breadcrumbs."""

import datetime as dt

from django.templatetags.static import static
from django.utils import timezone

from pycon_portugal_2027.site.context_processors import EVENT
from pycon_portugal_2027.site.context_processors import SOCIAL_MEDIA

SITE = EVENT["url"]
TICKET_SALES_OPEN = dt.date(2026, 11, 20)
ORGANIZATION_ID = f"{SITE}/#organization"
WEBSITE_ID = f"{SITE}/#website"
EVENT_ID = f"{SITE}/#event"


def organization():
    return {
        "@type": "Organization",
        "@id": ORGANIZATION_ID,
        "name": "PyCon Portugal",
        "url": "https://pycon.pt/",
        "logo": SITE + static("images/favicons/apple-touch-icon.png"),
        "email": EVENT["email"],
        # profiles of the organization; the Slack link is an invite, not a profile
        "sameAs": [url for name, url in SOCIAL_MEDIA.items() if name != "slack"],
    }


def website():
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "name": EVENT["name"],
        "url": f"{SITE}/",
        "inLanguage": "en",
        "publisher": {"@id": ORGANIZATION_ID},
    }


def event():
    return {
        "@type": "Event",
        "@id": EVENT_ID,
        "name": EVENT["name"],
        "description": EVENT["description"],
        "url": f"{SITE}/",
        "image": SITE + static("images/leiria/castle.jpg"),
        "startDate": "2027-04-22",
        "endDate": "2027-04-24",
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "inLanguage": "en",
        "location": {
            "@type": "Place",
            "name": "ULO – Universidade de Leiria e do Oeste, ESTG Campus 2",  # noqa: RUF001
            "url": f"{SITE}/information/venue/",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Campus 2 – Morro do Lena, Alto do Vieiro",  # noqa: RUF001
                "postalCode": "2411-901",
                "addressLocality": "Leiria",
                "addressCountry": "PT",
            },
        },
        "organizer": {"@id": ORGANIZATION_ID},
        "offers": [
            {
                "@type": "Offer",
                "name": f"{name} ticket (early bird)",
                "price": price,
                "priceCurrency": "EUR",
                "url": EVENT["tickets"],
                "validFrom": TICKET_SALES_OPEN.isoformat(),
                "availability": "https://schema.org/"
                + ("InStock" if timezone.localdate() >= TICKET_SALES_OPEN else "PreOrder"),
            }
            for name, price in (("Student", "30"), ("Individual", "75"), ("Business", "125"))
        ],
    }


def breadcrumbs(title, path):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": title, "item": SITE + path},
        ],
    }


def graph(*nodes):
    """Wrap ``nodes`` in one ``@graph`` document, always with the organization and website."""
    return {"@context": "https://schema.org", "@graph": [organization(), website(), *nodes]}

"""The important dates listed on the home page."""

import datetime as dt
from dataclasses import dataclass
from itertools import cycle
from itertools import groupby

from pycon_portugal_2027.site.context_processors import CFP_OPEN
from pycon_portugal_2027.site.context_processors import CONFERENCE_END
from pycon_portugal_2027.site.context_processors import CONFERENCE_START
from pycon_portugal_2027.site.context_processors import EVENT
from pycon_portugal_2027.site.context_processors import TICKET_SALES_OPEN

# Month headings take these colours in turn
COLOURS = ["magenta", "orange", "cyan", "purple", "amber"]


@dataclass(frozen=True)
class ImportantDate:
    label: str
    # the day it happens; for ``month_only`` dates, any day of its month
    on: dt.date
    # the last day of a date that spans several days
    until: dt.date | None = None
    # only the month is known, e.g. a month long review or a day still to be announced
    month_only: bool = False
    tba: bool = False
    href: str = ""
    # links to the pretix shop wait for ticket sales to open
    link_from: dt.date | None = None

    def done(self, today):
        """A date gets a check mark on its day, a ``month_only`` one once its month ends."""
        if self.month_only:
            return (today.year, today.month) > (self.on.year, self.on.month)
        return today >= self.on

    @property
    def day(self):
        if self.month_only:
            return ""
        if self.until:
            return f"{ordinal(self.on.day)} & {ordinal(self.until.day)}"
        return ordinal(self.on.day)


IMPORTANT_DATES = [
    ImportantDate(
        "Early-bird ticket sales open", TICKET_SALES_OPEN, href=EVENT["tickets"], link_from=TICKET_SALES_OPEN
    ),
    ImportantDate("Call for Participation opens", CFP_OPEN, href="/talks/cfp/"),
    ImportantDate("Grant applications open", dt.date(2026, 12, 1), href="/information/grants/"),
    ImportantDate("Call for Participation deadline", dt.date(2026, 12, 31), href="/talks/cfp/"),
    ImportantDate(
        "Content review & selection", dt.date(2027, 1, 1), month_only=True, href="/talks/selection_process/"
    ),
    ImportantDate(
        "Grant applications deadline", dt.date(2027, 1, 1), month_only=True, tba=True, href="/information/grants/"
    ),
    ImportantDate("Talks & schedule publication", dt.date(2027, 2, 1), month_only=True, href="/talks/schedule/"),
    ImportantDate(
        "Early-bird ticket sales close",
        dt.date(2027, 2, 1),
        month_only=True,
        tba=True,
        href=EVENT["tickets"],
        link_from=TICKET_SALES_OPEN,
    ),
    ImportantDate("Main conference", CONFERENCE_START, until=CONFERENCE_END - dt.timedelta(days=1)),
    ImportantDate("Workshops", CONFERENCE_END),
]


def ordinal(n):
    # 11th, 12th and 13th, but 1st, 2nd, 3rd, 21st...
    suffix = "th" if n % 100 in {11, 12, 13} else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def by_month(today):
    """Group the important dates by month, as the home page lists them on ``today``."""
    months = []
    colours = cycle(COLOURS)
    for _, dates in groupby(IMPORTANT_DATES, key=lambda date: (date.on.year, date.on.month)):
        dates = list(dates)  # noqa: PLW2901
        months.append(
            {
                "month": dates[0].on,
                "colour": next(colours),
                "dates": [
                    {
                        "label": date.label,
                        "day": date.day,
                        "tba": date.tba,
                        "href": date.href if not date.link_from or today >= date.link_from else "",
                        "external": date.href.startswith("https://"),
                        "done": date.done(today),
                    }
                    for date in dates
                ],
            }
        )
    return months

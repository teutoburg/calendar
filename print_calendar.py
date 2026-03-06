# -*- coding: utf-8 -*-

import calendar
from datetime import date
# import holidays
from io import StringIO

from more_itertools import first_true


class HTMLCalendarWithWeekNumbers(calendar.LocaleHTMLCalendar):
    cssclasses = [
        "mon", "tue", "wed", "thu", "fri",
        "sat weekend", "sun weekend",
    ]
    cssclass_noday = "noday"
    cssclass_month = "month"
    cssclass_year_head = "hidden"

    def formatweekheader(self) -> str:
        """Return row of weekday headers, with empty cell for week numbers."""
        headers = "".join(self.formatweekday(wd) for wd in self.iterweekdays())
        return f"<tr><th class=\"weeknumber\">&nbsp;</th>{headers}</tr>\n"

    def formatweek(
        self,
        theweek: list[tuple[int, int]],
        theyear: int = 0,
        themonth: int = 0,
    ) -> str:
        """Return a complete week as a table row with the ISO week numbers."""
        with StringIO() as stream:
            for day, weekday in theweek:
                stream.write(self.formatday(day, weekday))
                stream.write("\n")
            week_html = stream.getvalue()

        week_number: int | str
        try:
            week_number = self._get_weeknumber(theweek, theyear, themonth)
        except ValueError:
            week_number = "&nbsp;"

        out = (
            f"<tr>\n"
            f"<td class=\"weeknumber\">{week_number}</td>\n"
            f"{week_html}</tr>\n"
        )
        return out

    def formatmonthname(
        self,
        theyear: int,
        themonth: int,
        withyear: bool = True,
    ) -> str:
        """Override to change colspan."""
        monthrow = super().formatmonthname(theyear, themonth, withyear=withyear)
        monthrow.replace("colspan=\"7\"", "colspan=\"8\"")
        return monthrow

    def formatmonth(
        self,
        theyear: int,
        themonth: int,
        withyear: bool = True,
    ) -> str:
        """Need to override to supply formatweek with year and month."""
        with StringIO() as stream:
            stream.write(f"<table class=\"{self.cssclass_month}\">\n")
            stream.write(
                self.formatmonthname(theyear, themonth, withyear=withyear)
            )
            stream.write("\n")
            stream.write(self.formatweekheader())
            stream.write("\n")
            for week in self.monthdays2calendar(theyear, themonth):
                stream.write(self.formatweek(week, theyear, themonth))
            stream.write("</table>\n")
            out = stream.getvalue()
        return out

    @staticmethod
    def _get_weeknumber(
        theweek: list[tuple[int, int]],
        theyear: int,
        themonth: int,
    ) -> int:
        if theyear == 0 or themonth == 0:
            raise ValueError("need year and month for weeknumber")

        theday = first_true(day for day, _ in theweek)
        return date(theyear, themonth, theday).isocalendar().week


html_calendar = HTMLCalendarWithWeekNumbers(locale="de_AT")

with open("caltest.html", mode="wb") as file:
    file.write(html_calendar.formatyearpage(2026, width=1))

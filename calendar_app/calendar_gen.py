# -*- coding: utf-8 -*-

import calendar
from datetime import date
from io import StringIO

from more_itertools import first_true

from calendar_app.holidays_loader import UniversityHoliday


class HTMLCalendarWithWeekNumbers(calendar.LocaleHTMLCalendar):
    cssclasses = [
        "mon", "tue", "wed", "thu", "fri",
        "sat weekend", "sun weekend",
    ]
    cssclass_noday = "noday"
    cssclass_month = "month"
    cssclass_year_head = "hidden"

    def __init__(
        self,
        locale: str = "de_AT",
        public_holidays: dict[date, str] | None = None,
        university_holidays: list[UniversityHoliday] | None = None,
    ):
        super().__init__(locale=locale)
        self._public_holidays: dict[date, str] = public_holidays or {}
        self._university_holidays: list[UniversityHoliday] = university_holidays or []
        self._uni_lookup: dict[date, UniversityHoliday] = {}
        for uh in self._university_holidays:
            d = uh.start
            while d <= uh.end:
                self._uni_lookup[d] = uh
                d = date.fromordinal(d.toordinal() + 1)
        self._current_year = 0
        self._current_month = 0

    def formatweekheader(self) -> str:
        headers = "".join(self.formatweekday(wd) for wd in self.iterweekdays())
        return f"<tr><th class=\"weeknumber\">&nbsp;</th>{headers}</tr>\n"

    def formatday(self, day: int, weekday: int) -> str:
        if day == 0:
            return f'<td class="{self.cssclass_noday}">&nbsp;</td>'

        css_classes = [self.cssclasses[weekday]]
        label_html = ""

        d = date(self._current_year, self._current_month, day)

        if d in self._uni_lookup:
            css_classes.append("holiday-uni")

        if d in self._public_holidays:
            css_classes.append("holiday-public")
            label_html = (
                f'<span class="holiday-label">{self._public_holidays[d]}</span>'
            )
        elif d in self._uni_lookup:
            uh = self._uni_lookup[d]
            if uh.start == uh.end:
                label_html = (
                    f'<span class="holiday-label">{uh.name}</span>'
                )

        cls = " ".join(css_classes)
        return f'<td class="{cls}">{label_html}{day}</td>'

    def formatweek(
        self,
        theweek: list[tuple[int, int]],
        theyear: int = 0,
        themonth: int = 0,
    ) -> str:
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

        range_row = self._format_range_row(theweek, theyear, themonth)
        if range_row:
            out += range_row

        return out

    def _format_range_row(
        self,
        theweek: list[tuple[int, int]],
        theyear: int,
        themonth: int,
    ) -> str:
        if theyear == 0 or themonth == 0:
            return ""

        active_ranges: list[tuple[int, int, str]] = []
        i = 0
        while i < len(theweek):
            day, _ = theweek[i]
            if day == 0:
                i += 1
                continue
            d = date(theyear, themonth, day)
            if d in self._uni_lookup:
                uh = self._uni_lookup[d]
                if uh.start != uh.end:
                    start_idx = i
                    while (
                        i < len(theweek)
                        and theweek[i][0] != 0
                        and date(theyear, themonth, theweek[i][0]) in self._uni_lookup
                        and self._uni_lookup[date(theyear, themonth, theweek[i][0])] is uh
                    ):
                        i += 1
                    active_ranges.append((start_idx, i - 1, uh.name))
                    continue
            i += 1

        if not active_ranges:
            return ""

        cells = ['<td class="weeknumber"></td>']
        col = 0
        for start_idx, end_idx, name in active_ranges:
            while col < start_idx:
                cells.append("<td></td>")
                col += 1
            span = end_idx - start_idx + 1
            cells.append(f'<td colspan="{span}">{name}</td>')
            col = end_idx + 1
        while col < 7:
            cells.append("<td></td>")
            col += 1

        return f'<tr class="holiday-range-label">{"".join(cells)}</tr>\n'

    def formatmonthname(
        self,
        theyear: int,
        themonth: int,
        withyear: bool = True,
    ) -> str:
        monthrow = super().formatmonthname(theyear, themonth, withyear=withyear)
        monthrow = monthrow.replace("colspan=\"7\"", "colspan=\"8\"")
        return monthrow

    def formatmonth(
        self,
        theyear: int,
        themonth: int,
        withyear: bool = True,
    ) -> str:
        self._current_year = theyear
        self._current_month = themonth
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

    def generate_pages(
        self,
        year: int,
        start_month: int = 1,
        end_month: int = 12,
        css_path: str = "calendar.css",
    ) -> str:
        with StringIO() as stream:
            stream.write("<!DOCTYPE html>\n<html>\n<head>\n")
            stream.write("<meta charset=\"utf-8\">\n")
            stream.write(f"<title>Calendar {year}</title>\n")
            stream.write(f"<link rel=\"stylesheet\" href=\"{css_path}\">\n")
            stream.write("</head>\n<body>\n")
            for month in range(start_month, end_month + 1):
                stream.write(self.formatmonth(year, month))
                stream.write("\n")
            stream.write("</body>\n</html>\n")
            return stream.getvalue()

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

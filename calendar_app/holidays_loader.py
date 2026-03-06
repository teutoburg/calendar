from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import holidays as holidays_lib
import yaml


@dataclass
class UniversityHoliday:
    name: str
    start: date
    end: date


def get_public_holidays(year: int, locale: str) -> dict[date, str]:
    country = locale.split("_")[-1].upper()
    country_holidays = holidays_lib.country_holidays(country, years=year)
    return dict(country_holidays.items())


def load_university_holidays(filepath: str | None) -> list[UniversityHoliday]:
    if filepath is None:
        return []
    path = Path(filepath)
    if not path.exists():
        return []

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or "holidays" not in data:
        return []

    result: list[UniversityHoliday] = []
    for entry in data["holidays"]:
        name = entry["name"]
        if "date" in entry:
            d = _parse_date(entry["date"])
            result.append(UniversityHoliday(name=name, start=d, end=d))
        else:
            start = _parse_date(entry["start"])
            end = _parse_date(entry["end"])
            result.append(UniversityHoliday(name=name, start=start, end=end))

    return result


def expand_university_holidays(
    uni_holidays: list[UniversityHoliday],
) -> dict[date, UniversityHoliday]:
    result: dict[date, UniversityHoliday] = {}
    for uh in uni_holidays:
        d = uh.start
        while d <= uh.end:
            result[d] = uh
            d += timedelta(days=1)
    return result


def _parse_date(value: str | date) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))

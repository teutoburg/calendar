import argparse
import sys

from calendar_app.calendar_gen import HTMLCalendarWithWeekNumbers
from calendar_app.holidays_loader import (
    get_public_holidays,
    load_university_holidays,
)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Generate a printable HTML calendar with week numbers.",
    )
    parser.add_argument(
        "year",
        type=int,
        help="Calendar year (e.g. 2026)",
    )
    parser.add_argument(
        "-m", "--months",
        nargs=2,
        type=int,
        default=[1, 12],
        metavar=("START", "END"),
        help="Month range, inclusive (default: 1 12)",
    )
    parser.add_argument(
        "-o", "--output",
        default="calendar.html",
        help="Output HTML filename (default: calendar.html)",
    )
    parser.add_argument(
        "-l", "--locale",
        default="de_AT",
        help="Locale string (default: de_AT)",
    )
    parser.add_argument(
        "--holidays",
        default=None,
        metavar="FILE",
        help="Path to university holidays YAML file (optional)",
    )

    args = parser.parse_args(argv)

    start_month, end_month = args.months
    if not (1 <= start_month <= end_month <= 12):
        parser.error("Invalid month range. Must be 1 <= START <= END <= 12.")

    public_holidays = get_public_holidays(args.year, args.locale)
    uni_holidays = load_university_holidays(args.holidays)

    cal = HTMLCalendarWithWeekNumbers(
        locale=args.locale,
        public_holidays=public_holidays,
        university_holidays=uni_holidays,
    )

    html = cal.generate_pages(
        args.year,
        start_month=start_month,
        end_month=end_month,
    )

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Calendar written to {args.output}")


if __name__ == "__main__":
    main()

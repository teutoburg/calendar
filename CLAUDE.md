# Calendar Project — Developer Notes

## Project Overview
Printable HTML calendar generator with week numbers, public/university holiday support, and CLI interface. Outputs A4-landscape-optimized HTML that can be printed to PDF.

## Project Structure
```
calendar_app/
    __init__.py           # Re-exports HTMLCalendarWithWeekNumbers
    calendar_gen.py       # Core calendar class (extends LocaleHTMLCalendar)
    holidays_loader.py    # Public holidays (via `holidays` pkg) + university holidays (YAML)
    cli.py                # argparse CLI entry point
    __main__.py           # Enables `python -m calendar_app`
calendar.css              # Stylesheet (linked by generated HTML, not embedded)
tests/
    test_weeknumber.py    # Week number calculation + formatmonthname bug fix test
    test_holidays.py      # Holiday loading, expansion, public holiday lookup
test_holidays.yaml        # Example university holidays file
pyproject.toml            # Poetry project config
TODO.md                   # Original feature wishlist (all items now implemented)
```

## Usage
```bash
python -m calendar_app 2026                          # Full year, default locale de_AT
python -m calendar_app 2026 -m 3 6                   # March through June
python -m calendar_app 2026 --holidays holidays.yaml # With university holidays
python -m calendar_app 2026 -o output.html -l de_DE  # Custom output + locale
```

## Key Design Decisions

### Holiday System
- **Public holidays**: Derived automatically from locale using the `holidays` package. Country code is extracted from the locale string (e.g. `de_AT` → `AT`).
- **University holidays**: Loaded from an optional YAML file. Two formats: single `date:` or `start:`/`end:` range.
- **Range display**: Multi-day university holidays get a narrow spanning `<tr class="holiday-range-label">` below the week row instead of repeating the name in every cell. Single-day university holidays get an inline label like public holidays.

### CSS Shading Hierarchy (cascade order, lightest → strongest)
1. `.holiday-uni` — `#f0f0f0` (lightest)
2. `.weekend` — `#e0e0e0`
3. `.holiday-public` — `#c0c0c0` (strongest)

A public holiday on a weekend correctly gets the darkest shade because `.holiday-public` is declared last in CSS.

### Calendar Table Layout
- 8 columns: 1 week-number column (fixed 2em width) + 7 day columns
- `table-layout: fixed` for consistent column sizing
- `colspan="8"` on month name header (was a bug — originally said 8 but the `.replace()` result wasn't assigned)

## Dependencies
- `more-itertools` — `first_true` for finding the first real day in a week
- `holidays` — public holiday data by country
- `pyyaml` — parsing university holiday YAML files
- `pytest` (dev) — unit tests

## Running Tests
```bash
python -m pytest tests/ -v
```

## Previous State
The project was originally a single `print_calendar.py` script with hardcoded year (2026), locale (`de_AT`), and output filename (`caltest.html`). It was restructured into the `calendar_app` package and `print_calendar.py` was deleted. The `TODO.md` items (margins, holidays, shading, CLI, CSS cleanup, unit tests) have all been implemented.

## Notes
- The system running this has Python 3.11 (not 3.13 as pyproject.toml specifies). All code is compatible with 3.10+.
- Poetry is not on the shell PATH in this environment; `pip install` was used directly for dependency management.

# calendar

A printable HTML calendar generator with ISO week numbers, public holiday detection, and university holiday support. Designed for A4 landscape printing with clean grayscale shading.

## Installation

Requires Python 3.10 or later.

Install the dependencies:

```bash
pip install more-itertools holidays pyyaml
```

## Quick Start

Generate a full-year calendar for 2026:

```bash
python -m calendar_app 2026
```

This creates `calendar.html` in the current directory. Open it in a browser and use the print dialog (Ctrl+P) to export as PDF. The output is optimised for A4 landscape with one month per page.

## Usage

```
python -m calendar_app YEAR [OPTIONS]
```

### Arguments

| Argument | Description |
|---|---|
| `YEAR` | Calendar year to generate (required) |

### Options

| Option | Default | Description |
|---|---|---|
| `-m, --months START END` | `1 12` | Month range to include (inclusive) |
| `-o, --output FILE` | `calendar.html` | Output HTML filename |
| `-l, --locale LOCALE` | `de_AT` | Locale for weekday/month names and public holidays |
| `--holidays FILE` | *(none)* | Path to a university holidays YAML file |

### Examples

Generate only the summer semester (March through July):

```bash
python -m calendar_app 2026 -m 3 7
```

Generate a calendar with German locale and custom output path:

```bash
python -m calendar_app 2026 -l de_DE -o semester_plan.html
```

Generate a calendar with university holidays:

```bash
python -m calendar_app 2026 --holidays uni_holidays.yaml
```

## Holidays

### Public Holidays

Public holidays are detected automatically based on the locale. The country code is extracted from the locale string (e.g. `de_AT` uses Austrian holidays, `de_DE` uses German holidays). Each public holiday cell displays the holiday name in small text and receives the strongest background shading.

### University Holidays

University holidays are supplied via an optional YAML file. Two formats are supported:

**Single day:**

```yaml
holidays:
  - name: "Rektorstag"
    date: 2026-05-15
```

**Date range (inclusive):**

```yaml
holidays:
  - name: "Semesterferien"
    start: 2026-02-07
    end: 2026-03-01
```

A single file can contain any number of entries mixing both formats. See `test_holidays.yaml` for a complete example.

**How ranges are displayed:** Rather than repeating the name in every day cell, multi-day university holidays show a label row that spans the relevant days within each week. This keeps the calendar readable even for long breaks like summer holidays.

## Visual Design

### Shading Hierarchy

The calendar uses three levels of grayscale shading, designed to remain distinguishable when printed in black and white:

| Shading | Applies to | Color |
|---|---|---|
| Strongest | Public holidays | dark gray |
| Medium | Weekends (Sat/Sun) | medium gray |
| Lightest | University holidays | light gray |

When categories overlap (e.g. a public holiday falls on a weekend), the stronger shading wins.

### Layout

- One month per page when printed
- ISO week numbers in a narrow left-hand column
- A4 landscape orientation with minimal margins (3mm) to maximise table space
- Month and weekday names follow the selected locale

## Printing Tips

1. Open the generated HTML file in a browser
2. Open print dialog (Ctrl+P / Cmd+P)
3. Set the layout to **Landscape**
4. Set margins to **None** or **Minimum** (the CSS already handles margins)
5. Disable headers and footers for a cleaner result
6. Print or save as PDF

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

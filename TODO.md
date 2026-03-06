# TODO in calendar

## Reduce page margins
In the PDF print layout, there is too much whitespace around the table.
The calendar should use the whole available space of the page, with some reasonable printing margins.

## Support for holidays
Holidays shall be processed by adding a custom CSS class to the corresponding day cell.
Additionally, the name of the holiday shall be written at the top of the cell in small font, slightly faded gray.
There are two types of holidays, which differ mainly in their source:

### Public holidays
These should consider the locale, maybe using the `holidays` package.
The shading applied to these shall be the strongest (see also next section).

### University holidays
These need to be supplied from an external file.
The format for that needs to be specified, but shall use the YAML file format.
These can be single days or a range of days (e.g. summer break), each with a name / title.
Care shall be taken in how to display the range variant, avoiding repeating the title in each day cell of the range.
A good option might be to have a label spanning the portion of the date range found in each week (if it spans multiple weeks) and show the title once per week.
They are optional, meaning if no input file was provided, they are ignored.
The shading applied to these shall be the lightest (see also next section).

## Shading days
There shall be three levels of shading in the calendar:
1. Public holidays
2. Weekends
3. University holidays
Needs to be robust enough to handle e.g. a public holiday landing on a weekend.
Shadings may be colored but need to be distinguishable when printed in grayscale.

## Wrap in CLI
The script to run the calendar should be wrapped in a command line interface using argparse.
This should accept the year, months (min+max or range?), optional output filename, optional input filename for holidays.

## Cleanup CSS in general
Not sure how much can be done, but worth a look.

## Add unittests
Methods like `_get_weeknumber()` should be unit-tested using pytest.

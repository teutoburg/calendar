import pytest

from calendar_app.calendar_gen import HTMLCalendarWithWeekNumbers


class TestGetWeeknumber:
    def test_mid_month_week(self):
        # 2026-06-15 is a Monday, ISO week 25
        week = [(15, 0), (16, 1), (17, 2), (18, 3), (19, 4), (20, 5), (21, 6)]
        assert HTMLCalendarWithWeekNumbers._get_weeknumber(week, 2026, 6) == 25

    def test_year_boundary_jan1_in_previous_year_week(self):
        # 2026-01-01 is a Thursday, ISO week 1
        week = [(0, 0), (0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6)]
        assert HTMLCalendarWithWeekNumbers._get_weeknumber(week, 2026, 1) == 1

    def test_year_boundary_week53(self):
        # 2025-12-29 is a Monday, ISO week 1 of 2026
        week = [(29, 0), (30, 1), (31, 2), (0, 3), (0, 4), (0, 5), (0, 6)]
        assert HTMLCalendarWithWeekNumbers._get_weeknumber(week, 2025, 12) == 1

    def test_week_with_leading_padding(self):
        # March 2026 starts on Sunday; first week has padding
        week = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 6)]
        assert HTMLCalendarWithWeekNumbers._get_weeknumber(week, 2026, 3) == 9

    def test_error_on_zero_year(self):
        week = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6)]
        with pytest.raises(ValueError):
            HTMLCalendarWithWeekNumbers._get_weeknumber(week, 0, 1)

    def test_error_on_zero_month(self):
        week = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6)]
        with pytest.raises(ValueError):
            HTMLCalendarWithWeekNumbers._get_weeknumber(week, 2026, 0)


class TestFormatMonthName:
    def test_colspan_is_8(self):
        cal = HTMLCalendarWithWeekNumbers(locale="de_AT")
        result = cal.formatmonthname(2026, 1)
        assert 'colspan="8"' in result
        assert 'colspan="7"' not in result

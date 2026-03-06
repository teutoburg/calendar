import tempfile
from datetime import date
from pathlib import Path

import pytest

from calendar_app.holidays_loader import (
    UniversityHoliday,
    expand_university_holidays,
    get_public_holidays,
    load_university_holidays,
)


class TestLoadUniversityHolidays:
    def test_none_returns_empty(self):
        assert load_university_holidays(None) == []

    def test_nonexistent_file_returns_empty(self):
        assert load_university_holidays("/nonexistent/path.yaml") == []

    def test_single_day_entry(self):
        yaml_content = """
holidays:
  - name: "Rektorstag"
    date: 2026-05-15
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            f.write(yaml_content)
            f.flush()
            result = load_university_holidays(f.name)

        assert len(result) == 1
        assert result[0].name == "Rektorstag"
        assert result[0].start == date(2026, 5, 15)
        assert result[0].end == date(2026, 5, 15)
        Path(f.name).unlink()

    def test_range_entry(self):
        yaml_content = """
holidays:
  - name: "Semesterferien"
    start: 2026-02-07
    end: 2026-02-10
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            f.write(yaml_content)
            f.flush()
            result = load_university_holidays(f.name)

        assert len(result) == 1
        assert result[0].name == "Semesterferien"
        assert result[0].start == date(2026, 2, 7)
        assert result[0].end == date(2026, 2, 10)
        Path(f.name).unlink()


class TestExpandUniversityHolidays:
    def test_expand_range(self):
        uh = UniversityHoliday(
            name="Break", start=date(2026, 3, 2), end=date(2026, 3, 5)
        )
        expanded = expand_university_holidays([uh])
        assert len(expanded) == 4
        assert date(2026, 3, 2) in expanded
        assert date(2026, 3, 5) in expanded
        assert date(2026, 3, 6) not in expanded


class TestGetPublicHolidays:
    def test_known_austrian_holidays(self):
        holidays = get_public_holidays(2026, "de_AT")
        assert date(2026, 1, 1) in holidays
        assert date(2026, 12, 25) in holidays

    def test_returns_names(self):
        holidays = get_public_holidays(2026, "de_AT")
        assert isinstance(holidays[date(2026, 1, 1)], str)
        assert len(holidays[date(2026, 1, 1)]) > 0

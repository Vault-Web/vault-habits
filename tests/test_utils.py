from datetime import datetime

from beaverhabits.utils import format_date_difference, week_days


def s2d(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def test_date_diff_format():
    start = "2025-05-28"

    # diff >= 1y
    assert format_date_difference(s2d(start), s2d("2026-05-28")) == "1 years 1 days"
    assert (
        format_date_difference(s2d(start), s2d("2026-07-13"))
        == "1 years 1 months 16 days"
    )
    # diff >= 1m
    assert format_date_difference(s2d(start), s2d("2025-06-28")) == "1 months 1 days"
    assert format_date_difference(s2d(start), s2d("2025-06-29")) == "1 months 2 days"
    # diff >= 1w
    assert format_date_difference(s2d(start), s2d("2025-06-03")) == "7 days"
    assert format_date_difference(s2d(start), s2d("2025-06-05")) == "9 days"
    # diff < 1w
    assert format_date_difference(s2d(start), s2d("2025-05-27")) == ""
    assert format_date_difference(s2d(start), s2d("2025-05-28")) == "1 days"
    assert format_date_difference(s2d(start), s2d("2025-05-29")) == "2 days"


def test_week_days_cover_current_monday_to_sunday():
    assert week_days(s2d("2026-05-22")) == [
        s2d("2026-05-18"),
        s2d("2026-05-19"),
        s2d("2026-05-20"),
        s2d("2026-05-21"),
        s2d("2026-05-22"),
        s2d("2026-05-23"),
        s2d("2026-05-24"),
    ]

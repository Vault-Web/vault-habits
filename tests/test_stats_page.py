import datetime

from beaverhabits.frontend.stats_page import (
    percent_int,
    rolling_window_counts,
    thirty_day_progress_rates,
    window_label,
)
from beaverhabits.storage.dict import DictHabitList


def test_rolling_window_uses_registration_date_for_new_habit():
    today = datetime.date(2024, 5, 1)
    habits = DictHabitList(
        {
            "habits": [
                {
                    "name": "Leetcode",
                    "records": [{"day": today.strftime("%Y-%m-%d"), "done": True}],
                }
            ]
        }
    )

    completed, missed, tracked_days = rolling_window_counts(
        habits.habits[0], today, today, 30
    )

    assert completed == 1
    assert missed == 0
    assert tracked_days == 1
    assert percent_int(completed, tracked_days) == 100
    assert window_label(tracked_days) == "Last 1 day"


def test_30_day_progress_trend_uses_active_window_denominator():
    start = datetime.date(2024, 5, 18)
    today = datetime.date(2024, 5, 22)
    habits = DictHabitList(
        {
            "habits": [
                {
                    "name": "Clean",
                    "records": [
                        {"day": start.strftime("%Y-%m-%d"), "done": True},
                        {"day": today.strftime("%Y-%m-%d"), "done": True},
                    ],
                }
            ]
        }
    )

    _, rates = thirty_day_progress_rates(habits.habits[0], start, today)

    assert rates[-1] == 40
    assert max(rates) == 40


def test_30_day_progress_trend_is_zero_without_completions():
    start = datetime.date(2024, 5, 22)
    today = datetime.date(2024, 5, 26)
    habits = DictHabitList(
        {
            "habits": [
                {
                    "name": "Call mom",
                    "records": [],
                }
            ]
        }
    )

    _, rates = thirty_day_progress_rates(habits.habits[0], start, today)

    assert rates
    assert max(rates) == 0

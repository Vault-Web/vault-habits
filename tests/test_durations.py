import datetime

import pytest

from beaverhabits.core.durations import format_duration, parse_duration_minutes
from beaverhabits.storage.dict import DictHabitList


def test_format_duration():
    assert format_duration(None) == ""
    assert format_duration(0) == ""
    assert format_duration(25) == "25m"
    assert format_duration(60) == "1h"
    assert format_duration(95) == "1h 35m"


def test_parse_duration_minutes():
    assert parse_duration_minutes("") is None
    assert parse_duration_minutes(None) is None
    assert parse_duration_minutes("45") == 45
    assert parse_duration_minutes("-10") == 0
    assert parse_duration_minutes("abc") is None


@pytest.mark.asyncio
async def test_habit_tick_stores_duration_minutes():
    today = datetime.date(2026, 5, 27)
    habits = DictHabitList({"habits": [{"name": "Run", "records": []}]})

    record = await habits.habits[0].tick(today, True, "Felt good", 35)

    assert record.duration_minutes == 35
    assert habits.habits[0].record_by(today).duration_minutes == 35

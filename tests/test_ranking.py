import datetime

from beaverhabits.storage.dict import DictHabitList
from beaverhabits.views import VaultWebRankingRow, _compute_ranking_scores


def test_weekly_score_drives_ranking_score_more_than_30_day_context():
    comeback = VaultWebRankingRow(
        "comeback",
        active_habits=2,
        completion_rate=20.0,
        weekly_score=80.0,
        avg_streak_days=1.0,
    )
    legacy = VaultWebRankingRow(
        "legacy",
        active_habits=2,
        completion_rate=95.0,
        weekly_score=30.0,
        avg_streak_days=1.0,
    )

    assert comeback.total_score > legacy.total_score


def test_current_week_score_uses_only_elapsed_week_days():
    today = datetime.date(2024, 5, 22)
    habits = DictHabitList(
        {
            "habits": [
                {
                    "name": "Run",
                    "records": [
                        {"day": "2024-05-20", "done": True},
                        {"day": "2024-05-22", "done": True},
                    ],
                }
            ]
        }
    )

    _, weekly_score, _, week_done, week_possible = _compute_ranking_scores(
        habits.habits, today, registered_on=datetime.date(2024, 5, 20)
    )

    assert week_done == 2
    assert week_possible == 3
    assert round(weekly_score) == 67

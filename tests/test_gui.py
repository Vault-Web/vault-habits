import datetime

from nicegui import ui
from nicegui.testing import User

from beaverhabits.frontend.add_page import add_page_ui
from beaverhabits.frontend.habit_page import habit_page_ui
from beaverhabits.frontend.index_page import index_page_ui
from beaverhabits.frontend.ranking_page import ranking_page_ui
from beaverhabits.frontend.stats_page import stats_page_ui
from beaverhabits.views import VaultWebRankingRow, dummy_habit_list

# Test cases:
# https://github.com/zauberzeug/nicegui/tree/main/tests


def dummy_today():
    return datetime.date(2024, 5, 1)


def dummy_days(count):
    today = dummy_today()
    return [today - datetime.timedelta(days=i) for i in reversed(range(count))]


async def test_index_page(user: User) -> None:
    days = dummy_days(7)
    habits = dummy_habit_list(days)

    @ui.page("/")
    def page():
        index_page_ui(days, habits)

    await user.open("/")
    await user.should_see("Habits")
    await user.should_see("Add habit")


async def test_add_page(user) -> None:
    days = dummy_days(7)
    habits = dummy_habit_list(days)

    @ui.page("/")
    def page():
        add_page_ui(habits)

    await user.open("/")
    await user.should_see("Habits")


async def test_habit_detail_page(user) -> None:
    days = dummy_days(7)
    today = days[-1]
    habits = dummy_habit_list(days)
    habit = habits.habits[0]

    @ui.page("/")
    def page():
        habit_page_ui(today, habit)

    await user.open("/")
    await user.should_see("Order pizz")


async def test_habit_stats_page(user) -> None:
    days = dummy_days(7)
    today = days[-1]
    habits = dummy_habit_list(days)

    @ui.page("/")
    def page():
        stats_page_ui(today, habits, registered_on=days[0])

    await user.open("/")
    await user.should_see("Order pizz")
    await user.should_see("Last 7 days")
    await user.should_see("Today")
    await user.should_see("Year")


async def test_ranking_page(user) -> None:
    @ui.page("/")
    def page():
        ranking_page_ui(
            [
                VaultWebRankingRow(
                    "deniz",
                    active_habits=3,
                    completion_rate=85.0,
                    weekly_score=71.4,
                    avg_streak_days=5.0,
                    is_current_user=True,
                ),
                VaultWebRankingRow(
                    "ada",
                    active_habits=2,
                    completion_rate=60.0,
                    weekly_score=42.9,
                    avg_streak_days=2.0,
                ),
            ]
        )

    await user.open("/")
    await user.should_see("Weekly Ranking")
    await user.should_see("deniz")
    await user.should_see("71%")

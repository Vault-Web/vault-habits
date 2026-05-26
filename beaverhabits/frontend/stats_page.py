import calendar
import datetime

from nicegui import ui

from beaverhabits.configs import settings
from beaverhabits.frontend.components import redirect
from beaverhabits.frontend.components import link
from beaverhabits.frontend.layout import layout
from beaverhabits.storage.meta import get_habit_heatmap_path
from beaverhabits.storage.storage import Habit, HabitList, HabitListBuilder, HabitStatus

_PRIMARY_SOLID = "rgba(103,150,207,1)"
_PRIMARY_FADE = "rgba(103,150,207,0.18)"
_PRIMARY_ZERO = "rgba(103,150,207,0)"
_SUCCESS_SOLID = "rgba(35,134,54,1)"
_WARNING_SOLID = "rgba(245,158,11,1)"


def week_start_of(date: datetime.date) -> datetime.date:
    days_offset = (date.weekday() - settings.FIRST_DAY_OF_WEEK) % 7
    return date - datetime.timedelta(days=days_offset)


def heatmap_years(registered_on: datetime.date, today: datetime.date) -> list[int]:
    return list(range(today.year, registered_on.year - 1, -1))


def weekday_names() -> list[str]:
    return [calendar.day_abbr[(settings.FIRST_DAY_OF_WEEK + i) % 7] for i in range(7)]


def iter_days(start: datetime.date, end: datetime.date):
    day = start
    while day <= end:
        yield day
        day += datetime.timedelta(days=1)


def format_percent(value: int, total: int) -> str:
    if total <= 0:
        return "0%"
    return f"{round(value / total * 100)}%"


def percent_int(value: int, total: int) -> int:
    if total <= 0:
        return 0
    return round(value / total * 100)


def current_streak(
    habit: Habit, registered_on: datetime.date, today: datetime.date
) -> int:
    streak = 0
    day = today
    while day >= registered_on:
        if not habit.record_by(day) or not habit.record_by(day).done:
            break
        streak += 1
        day -= datetime.timedelta(days=1)
    return streak


def best_habit(
    active_habits: list[Habit], registered_on: datetime.date, today: datetime.date
):
    total_days = max((today - registered_on).days + 1, 1)
    return max(
        active_habits,
        key=lambda habit: (
            habit.ticked_count(registered_on, today) / total_days,
            habit.name,
        ),
        default=None,
    )


def completed_today(active_habits: list[Habit], today: datetime.date) -> int:
    return sum(
        1
        for habit in active_habits
        if habit.record_by(today) and habit.record_by(today).done
    )


def perfect_days(
    active_habits: list[Habit], registered_on: datetime.date, today: datetime.date
) -> int:
    if not active_habits:
        return 0
    total = 0
    for day in iter_days(registered_on, today):
        if all(
            habit.record_by(day) and habit.record_by(day).done
            for habit in active_habits
        ):
            total += 1
    return total


def week_completion(
    active_habits: list[Habit], registered_on: datetime.date, today: datetime.date
):
    start = max(registered_on, week_start_of(today))
    days = max((today - start).days + 1, 1)
    possible = days * len(active_habits)
    done = sum(habit.ticked_count(start, today) for habit in active_habits)
    return done, possible


def rolling_window_counts(
    habit: Habit, registered_on: datetime.date, today: datetime.date, days: int
) -> tuple[int, int, int]:
    start = today - datetime.timedelta(days=days - 1)
    tracked_start = max(start, registered_on)
    tracked_days = max((today - tracked_start).days + 1, 0)
    completions = habit.ticked_count(tracked_start, today) if tracked_days else 0
    missed = max(tracked_days - completions, 0)
    return completions, missed, tracked_days


def window_label(tracked_days: int) -> str:
    if tracked_days == 1:
        return "Last 1 day"
    return "Last 30 days" if tracked_days >= 30 else f"Last {tracked_days} days"


def completion_donut(completions: int, missed: int, tracked_days: int):
    total = max(tracked_days, 0)
    rate = percent_int(completions, total)
    chart = ui.echart(
        {
            "tooltip": {"trigger": "item", "formatter": "{b}: {c} days"},
            "legend": {"show": False},
            "series": [
                {
                    "type": "pie",
                    "radius": ["68%", "88%"],
                    "center": ["50%", "50%"],
                    "avoidLabelOverlap": True,
                    "label": {
                        "show": True,
                        "position": "center",
                        "formatter": f"{rate}%",
                        "fontSize": 20,
                        "fontWeight": 700,
                    },
                    "labelLine": {"show": False},
                    "data": [
                        {
                            "value": completions,
                            "name": "Completed",
                            "itemStyle": {"color": _SUCCESS_SOLID},
                        },
                        {
                            "value": missed,
                            "name": "Missed",
                            "itemStyle": {"color": _WARNING_SOLID},
                        },
                    ],
                    "animation": False,
                }
            ],
        }
    )
    chart.classes("vault-stats-donut")


def thirty_day_progress_rates(
    habit: Habit, registered_on: datetime.date, today: datetime.date
) -> tuple[list[str], list[int]]:
    window_start = today - datetime.timedelta(days=29)
    chart_start = max(registered_on, window_start)
    tracked_days = max((today - chart_start).days + 1, 1)
    labels: list[str] = []
    rates: list[int] = []
    for day in iter_days(chart_start, today):
        rates.append(percent_int(habit.ticked_count(chart_start, day), tracked_days))
        labels.append(day.strftime("%d %b"))
    return labels, rates


def progress_trend(habit: Habit, registered_on: datetime.date, today: datetime.date):
    labels, rates = thirty_day_progress_rates(habit, registered_on, today)
    if not rates or max(rates) == 0:
        empty_progress_state()
        return

    chart = ui.echart(
        {
            "tooltip": {"trigger": "axis"},
            "xAxis": {
                "type": "category",
                "data": labels,
                "boundaryGap": False,
                "axisLabel": {"show": len(labels) <= 8, "fontSize": 10},
                "axisTick": {"show": False},
            },
            "yAxis": {
                "type": "value",
                "min": 0,
                "max": 100,
                "position": "right",
                "axisLabel": {"formatter": "{value}%", "fontSize": 10},
                "splitLine": {"lineStyle": {"color": "rgba(128,128,128,0.16)"}},
            },
            "series": [
                {
                    "type": "line",
                    "name": "30-day progress",
                    "data": rates,
                    "smooth": 0.25,
                    "showSymbol": len(rates) <= 8,
                    "symbolSize": 5,
                    "itemStyle": {"color": _PRIMARY_SOLID},
                    "lineStyle": {"color": _PRIMARY_SOLID, "width": 2},
                    "areaStyle": {
                        "color": {
                            "type": "linear",
                            "x": 0,
                            "y": 0,
                            "x2": 0,
                            "y2": 1,
                            "colorStops": [
                                {"offset": 0, "color": _PRIMARY_FADE},
                                {"offset": 1, "color": _PRIMARY_ZERO},
                            ],
                        }
                    },
                    "animation": False,
                }
            ],
            "grid": {"top": 12, "bottom": 22, "left": 8, "right": 36},
        }
    )
    chart.classes("vault-progress-trend-chart")


def empty_progress_state():
    with ui.element("div").classes("vault-progress-empty"):
        ui.label("0%").classes("vault-progress-empty-value")
        ui.label("No completed days yet.").classes("vault-progress-empty-label")


def habit_metric_tile(value: str, label: str, icon: str | None = None):
    with ui.element("div").classes("vault-habit-metric-tile"):
        with ui.row().classes("items-center gap-1 no-wrap"):
            if icon:
                ui.icon(icon).classes("vault-habit-metric-icon")
            ui.label(value).classes("vault-habit-metric-value")
        ui.label(label).classes("vault-habit-metric-label")


def heatmap_level(done: bool, day: datetime.date, today: datetime.date) -> str:
    if day > today:
        return "future"
    return "done" if done else "empty"


def year_week_starts(year: int, today: datetime.date) -> list[datetime.date]:
    year_start = datetime.date(year, 1, 1)
    year_end = min(today, datetime.date(year, 12, 31))
    week_start = week_start_of(year_start)
    last_week_start = week_start_of(year_end)

    weeks: list[datetime.date] = []
    while week_start <= last_week_start:
        weeks.append(week_start)
        week_start += datetime.timedelta(weeks=1)
    return weeks


def year_headers(year: int, weeks: list[datetime.date]) -> list[str]:
    labels: list[str] = []
    prev_month = None
    for week_start in weeks:
        label_day = max(week_start, datetime.date(year, 1, 1))
        if label_day.year != year:
            labels.append("")
            continue
        if label_day.month != prev_month:
            labels.append(calendar.month_abbr[label_day.month])
            prev_month = label_day.month
        else:
            labels.append("")
    return labels


def _render_contribution_heatmap(
    habit: Habit, year: int, registered_on: datetime.date, today: datetime.date
):
    weeks = year_week_starts(year, today)
    headers = year_headers(year, weeks)
    weekday_labels = weekday_names()
    columns_style = f"grid-template-columns: repeat({len(weeks)}, 13px) 28px;"

    with ui.element("div").classes("vault-scroll-surface") as scroll_div:
        with ui.element("div").classes("vault-contribution-map"):
            with (
                ui.element("div")
                .classes("vault-contribution-months")
                .style(columns_style)
            ):
                for header in headers:
                    ui.label(header).classes("vault-contribution-month")
                ui.label("").classes("vault-contribution-weekday")

            for weekday_index, weekday in enumerate(weekday_labels):
                with (
                    ui.element("div")
                    .classes("vault-contribution-row")
                    .style(columns_style)
                ):
                    for week_start in weeks:
                        day = week_start + datetime.timedelta(days=weekday_index)
                        if day < registered_on or day.year != year:
                            ui.element("span").classes(
                                "vault-contribution-cell is-blank"
                            )
                            continue

                        record = habit.record_by(day)
                        is_done = bool(record and record.done)
                        level = heatmap_level(is_done, day, today)
                        cell = ui.element("span").classes(
                            f"vault-contribution-cell is-{level}"
                        )
                        state = "completed" if is_done else "not completed"
                        cell.props(f'aria-label="{day.strftime("%d %b %Y")}: {state}"')
                        with cell:
                            ui.tooltip(f"{day.strftime('%d %b %Y')}: {state}")

                    ui.label(weekday[:3]).classes("vault-contribution-weekday")

    ui.run_javascript(
        f"setTimeout(function(){{"
        f"  var el = document.getElementById('c{scroll_div.id}');"
        f"  if (el) el.scrollLeft = el.scrollWidth;"
        f"}}, 40)"
    )


def progress_card(habit: Habit, registered_on: datetime.date, today: datetime.date):
    target = get_habit_heatmap_path(habit)
    completions = habit.ticked_count(registered_on, today)
    total_days = max((today - registered_on).days + 1, 1)
    recent_completions, recent_missed, tracked_days = rolling_window_counts(
        habit, registered_on, today, 30
    )
    recent_label = window_label(tracked_days)
    streak = current_streak(habit, registered_on, today)
    years = heatmap_years(registered_on, today)
    selected_year = [today.year]

    # Both the year tabs AND the heatmap live inside one refreshable so that
    # clicking a tab updates both the active highlight and the displayed heatmap.
    @ui.refreshable
    def year_section():
        with ui.row().classes("items-center gap-0 w-full"):
            ui.label("Year").classes("vault-stats-section-label")
            ui.space()
            for year in years:
                btn = ui.button(
                    str(year),
                    on_click=lambda y=year: _select_year(y),
                )
                btn.props("flat dense")
                btn.classes("vault-stats-year-tab")
                if year == selected_year[0]:
                    btn.classes("vault-stats-year-tab--active")
        _render_contribution_heatmap(habit, selected_year[0], registered_on, today)

    def _select_year(y: int):
        selected_year[0] = y
        year_section.refresh()

    with ui.card().classes("vault-stats-card no-shadow gap-4 p-3"):
        with ui.row().classes("vault-stats-card-head items-start no-wrap"):
            link(habit.name, target).classes("vault-stats-habit-name")
            ui.space()
            with ui.row().classes("vault-stats-inline-metrics no-wrap"):
                habit_metric_tile(
                    f"{streak}d", "current streak", "local_fire_department"
                )
                habit_metric_tile(f"{completions}/{total_days}", "all time")
                habit_metric_tile(
                    f"{recent_completions}/{tracked_days}", recent_label.lower()
                )

        with ui.element("section").classes("vault-habit-insights"):
            with ui.element("div").classes("vault-habit-donut-panel"):
                ui.label(recent_label).classes("vault-stats-section-label")
                completion_donut(recent_completions, recent_missed, tracked_days)
                with ui.element("div").classes("vault-donut-legend"):
                    for color_class, value, label in (
                        ("is-done", recent_completions, "completed"),
                        ("is-missed", recent_missed, "missed"),
                    ):
                        with ui.element("div").classes("vault-donut-legend-item"):
                            ui.element("span").classes(
                                f"vault-donut-legend-dot {color_class}"
                            )
                            ui.label(f"{value} {label}").classes(
                                "vault-donut-legend-label"
                            )

            with ui.element("div").classes("vault-habit-trend-panel"):
                ui.label("Progress trend").classes("vault-stats-section-label")
                if recent_completions:
                    progress_trend(habit, registered_on, today)
                else:
                    empty_progress_state()
                ui.label(
                    f"{recent_label}: {recent_completions} completed, {recent_missed} missed."
                ).classes("vault-stats-helper")

        with ui.element("section").classes("vault-stats-years"):
            year_section()


def stats_summary(
    active_habits: list[Habit], registered_on: datetime.date, today: datetime.date
):
    completions = sum(
        habit.ticked_count(registered_on, today) for habit in active_habits
    )
    days = max((today - registered_on).days + 1, 1)
    possible = days * len(active_habits)
    today_done = completed_today(active_habits, today)
    week_done, week_possible = week_completion(active_habits, registered_on, today)
    perfect_count = perfect_days(active_habits, registered_on, today)
    top_habit = best_habit(active_habits, registered_on, today)
    weeks = max((today - registered_on).days // 7 + 1, 1)

    with ui.element("section").classes("vault-stats-overview"):
        with ui.row().classes("vault-stats-overview-head items-end"):
            with ui.column().classes("gap-0"):
                ui.label("Progress").classes("vault-stats-title")
                ui.label(
                    f"Since {registered_on.strftime('%d %b %Y')} · {today.strftime('%d %b %Y')}"
                ).classes("vault-stats-range")
            ui.space()
            ui.label(f"{weeks} weeks tracked").classes("vault-stats-pill")

        with ui.row().classes("vault-stats-summary w-full"):
            for value, label, tone in (
                (len(active_habits), "Active habits", "neutral"),
                (f"{today_done}/{len(active_habits)}", "Today", "success"),
                (format_percent(week_done, week_possible), "This week", "primary"),
                (format_percent(completions, possible), "All-time rate", "primary"),
                (perfect_count, "Perfect days", "warm"),
                (top_habit.name if top_habit else "-", "Best habit", "success"),
            ):
                with ui.element("div").classes(f"vault-stat is-{tone}"):
                    ui.label(str(value)).classes("vault-stat-value")
                    ui.label(label).classes("vault-stat-label")

        ui.label(
            "Each square is one day. Darker squares mean the habit was completed."
        ).classes("vault-stats-helper")


@ui.refreshable
def stats_page_ui(
    today: datetime.date, habits: HabitList, registered_on: datetime.date
):
    active_habits = HabitListBuilder(habits).status(HabitStatus.ACTIVE).build()
    if not active_habits:
        redirect("/add")
        return

    registered_on = min(registered_on, today)

    with layout(habit_list=habits):
        stats_summary(active_habits, registered_on, today)

        with ui.element("div").classes("vault-stats-grid"):
            for habit in active_habits:
                progress_card(habit, registered_on, today)

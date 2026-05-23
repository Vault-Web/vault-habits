import datetime
from typing import List

from nicegui import ui

from beaverhabits import utils
from beaverhabits.configs import settings
from beaverhabits.core.completions import get_habit_date_completion
from beaverhabits.frontend import javascript, textarea
from beaverhabits.frontend.components import (
    HabitCheckBox,
    IndexStreakBadge,
    IndexTotalBadge,
    filter_habits_with_tags,
    habit_name_menu,
    habits_by_tags,
    note_tick,
    tag_filter_component,
)
from beaverhabits.frontend.layout import layout
from beaverhabits.logger import logger
from beaverhabits.storage.storage import (
    Habit,
    HabitList,
    HabitListBuilder,
    HabitOrder,
    HabitStatus,
)

NAME_COLS, DATE_COLS = settings.INDEX_HABIT_NAME_COLUMNS, 2
COUNT_BADGE_COLS = 2 if settings.INDEX_SHOW_HABIT_COUNT else 0
COUNT_BADGE_COLS += 2 if settings.INDEX_SHOW_HABIT_STREAK else 0
LEFT_CLASSES, RIGHT_CLASSES = (
    # grid 5
    f"col-span-{NAME_COLS} truncate max-w-[{24 * NAME_COLS}px]",
    # grid 2 2 2 2 2
    f"col-span-{DATE_COLS} px-1 place-self-center",
)
COMPAT_CLASSES = "pl-4 pr-0 py-0 dark:shadow-none"

# Sticky date row for long habit list
STICKY_STYLES = "position: sticky; top: 0; z-index: 1;"


def grid(columns, rows):
    g = ui.grid(columns=columns, rows=rows)
    g.classes("w-full gap-0 items-center")
    return g


def week_headers(days: list[datetime.date]):
    for day in days:
        yield day.strftime("%a")
    if settings.INDEX_SHOW_HABIT_STREAK:
        yield "Stk"
    if settings.INDEX_SHOW_HABIT_COUNT:
        yield "Sum"


def day_headers(days: list[datetime.date]):
    for day in days:
        yield day.strftime("%d")
    if settings.INDEX_SHOW_HABIT_STREAK:
        yield "*"
    if settings.INDEX_SHOW_HABIT_COUNT:
        yield "#"


class HabitWeekCard(ui.card):
    def __init__(self, habit: Habit) -> None:
        super().__init__()
        self.habit = habit
        self.props("draggable")
        self.classes(
            f"{COMPAT_CLASSES} vault-index-card vault-week-item theme-card-shadow"
        )


def habit_row(habit: Habit, days: list[datetime.date], today: datetime.date):
    with ui.row().classes(f"{LEFT_CLASSES} no-wrap items-center gap-1"):
        ui.icon("drag_indicator").classes("vault-week-drag-handle")
        name = habit_name_menu(habit, index_page_ui.refresh)
        name.classes("truncate min-w-0")
        name.props(f'role="heading" aria-level="2" aria-label="{habit.name}"')

    status_map = get_habit_date_completion(habit, min(days), max(days))
    for day in days:
        status = status_map.get(day, [])
        checkbox = HabitCheckBox(
            status, habit, today, day, refresh=habit_list_ui.refresh
        )
        checkbox.classes(RIGHT_CLASSES)
        # checkbox.classes("theme-icon-lazy invisible")

    if settings.INDEX_SHOW_HABIT_STREAK:
        IndexStreakBadge(today, habit).classes(RIGHT_CLASSES)

    if settings.INDEX_SHOW_HABIT_COUNT:
        IndexTotalBadge(today, habit).classes(RIGHT_CLASSES)


async def week_item_drop(e, habit_list: HabitList):
    dragged = ui.context.client.elements[int(e.args["id"][1:])]
    assert dragged.parent_slot is not None
    dragged.move(target_index=e.args["new_index"])

    order = []
    for item in dragged.parent_slot:
        if not isinstance(item, HabitWeekCard):
            continue
        habit_id = str(item.habit.id)
        if habit_id not in order:
            order.append(habit_id)

    habit_list.order = order
    habit_list.order_by = HabitOrder.MANUALLY
    logger.info(f"Weekly habit order: {order}")


def enable_week_sorting(habit_list: HabitList):
    ui.add_body_html("""
        <script type="module">
        import '/statics/libs/sortable.min.js';
        const initializeWeekSorting = () => {
            document.querySelectorAll('.vault-week-sortable').forEach((list) => {
                if (list.dataset.weekSortable === 'true') return;
                list.dataset.weekSortable = 'true';
                Sortable.create(list, {
                    animation: 150,
                    draggable: '.vault-week-item',
                    handle: '.vault-week-drag-handle',
                    ghostClass: 'opacity-50',
                    onEnd: (evt) => emitEvent('week_item_drop', {
                        id: evt.item.id,
                        new_index: evt.newIndex,
                    }),
                });
            });
        };
        document.addEventListener('DOMContentLoaded', initializeWeekSorting);
        new MutationObserver(initializeWeekSorting).observe(document.body, {
            childList: true,
            subtree: true,
        });
        </script>
        """)
    ui.on("week_item_drop", lambda e: week_item_drop(e, habit_list))


@ui.refreshable
def habit_list_ui(
    days: list[datetime.date], active_habits: List[Habit], today: datetime.date
):
    if settings.ENABLE_TAG_FILTERS:
        active_habits = filter_habits_with_tags(active_habits)

    # Total cloumn for each row
    columns = NAME_COLS + len(days) * DATE_COLS + COUNT_BADGE_COLS

    with ui.column().classes("vault-index-list"):
        # Date Headers
        with (
            grid(columns, 2)
            .classes(f"{COMPAT_CLASSES} vault-index-header")
            .style(STICKY_STYLES) as g
        ):
            g.props('aria-hidden="true"').classes("theme-header-date")
            for it in (week_headers(days), day_headers(days)):
                ui.label("").classes(LEFT_CLASSES)
                for label in it:
                    ui.label(label).classes(RIGHT_CLASSES)

        with ui.column().classes("vault-week-sortable w-full gap-2"):
            # Habit Rows
            groups = habits_by_tags(active_habits)

            for tag, habit_list in groups.items():
                if not habit_list:
                    continue

                for habit in habit_list:
                    with HabitWeekCard(habit):
                        with grid(columns, 1):
                            habit_row(habit, days, today)

                ui.space()


def get_active_habits(habits: HabitList) -> List[Habit]:
    return HabitListBuilder(habits).status(HabitStatus.ACTIVE).build()


def refresh_habit_list_when_today_changes(
    days: list[datetime.date], habits: HabitList
) -> None:
    rendered_days = days

    async def refresh_if_needed() -> None:
        nonlocal rendered_days
        today = await utils.get_user_today_date()
        new_days = await utils.current_week_days()
        if new_days == rendered_days:
            return
        rendered_days = new_days
        if settings.INDEX_HABIT_DATE_REVERSE:
            new_days = list(reversed(new_days))
        habit_list_ui.refresh(new_days, get_active_habits(habits), today)

    ui.timer(60, refresh_if_needed, immediate=False)


@ui.refreshable
def index_page_ui(
    days: list[datetime.date], habits: HabitList, today: datetime.date | None = None
):
    active_habits = get_active_habits(habits)
    today = today or max(days)
    if settings.INDEX_HABIT_DATE_REVERSE:
        days = list(reversed(days))

    with layout(habit_list=habits):
        if settings.ENABLE_TAG_FILTERS:
            tag_filter_component(active_habits, refresh=habit_list_ui.refresh)

        if not active_habits:
            ui.label("List is empty.").classes("mx-auto w-80")
            return
        habit_list_ui(days, active_habits, today)
        enable_week_sorting(habits)

    # placeholder to preload js cache (daily notes)
    textarea.Textarea("").classes("hidden").props('aria-hidden="true"')
    ui.input("").classes("hidden").props('aria-hidden="true"')

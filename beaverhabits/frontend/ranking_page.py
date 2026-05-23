from nicegui import ui

from beaverhabits.frontend.layout import layout
from beaverhabits.views import VaultWebRankingRow


def _fmt_pct(value: float) -> str:
    return f"{round(value)}%"


def _fmt_streak(days: float) -> str:
    d = round(days)
    return f"{d}d"


def ranking_page_ui(rows: list[VaultWebRankingRow]):
    with layout(title="Ranking"):
        ui.label("Vault Web Ranking").classes("text-xl font-bold")

        if not rows:
            ui.label("No Vault Web habit completions yet.").classes(
                "text-grey-7 dark:text-grey-5"
            )
            return

        with ui.element("div").classes("vault-ranking-board"):
            for rank, row in enumerate(rows, start=1):
                classes = "vault-ranking-row"
                if row.is_current_user:
                    classes += " is-current"

                with ui.element("div").classes(classes):
                    ui.label(str(rank)).classes("vault-ranking-rank")
                    with ui.column().classes("gap-0 min-w-0"):
                        with ui.row().classes("items-center gap-2 no-wrap"):
                            ui.label(row.display_name).classes("vault-ranking-name")
                            if row.is_current_user:
                                ui.badge("You").props("outline color=primary")
                        habits = "habit" if row.active_habits == 1 else "habits"
                        ui.label(f"{row.active_habits} active {habits}").classes(
                            "vault-ranking-subtext"
                        )
                    with ui.element("div").classes("vault-ranking-scores"):
                        with ui.element("div").classes("vault-ranking-score-item"):
                            ui.label(_fmt_pct(row.completion_rate)).classes(
                                "vault-ranking-score-value"
                            )
                            ui.label("30d rate").classes("vault-ranking-score-label")
                        with ui.element("div").classes("vault-ranking-score-item"):
                            ui.label(_fmt_pct(row.weekly_score)).classes(
                                "vault-ranking-score-value"
                            )
                            ui.label("week").classes("vault-ranking-score-label")
                        with ui.element("div").classes("vault-ranking-score-item"):
                            ui.label(_fmt_streak(row.avg_streak_days)).classes(
                                "vault-ranking-score-value"
                            )
                            ui.label("streak").classes("vault-ranking-score-label")

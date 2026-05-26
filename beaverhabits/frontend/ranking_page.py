from nicegui import ui

from beaverhabits.frontend.layout import layout
from beaverhabits.views import VaultWebRankingRow


def _fmt_pct(value: float) -> str:
    return f"{round(value)}%"


def _fmt_streak(days: float) -> str:
    d = round(days)
    return f"{d}d"


def _fmt_record(row: VaultWebRankingRow) -> str:
    if row.week_possible <= 0:
        return "0/0"
    return f"{row.week_done}/{row.week_possible}"


def ranking_page_ui(rows: list[VaultWebRankingRow]):
    with layout(title="Ranking"):
        with ui.column().classes("gap-0"):
            ui.label("Weekly Ranking").classes("text-xl font-bold")
            ui.label("Resets every week, so everyone can catch up.").classes(
                "vault-ranking-intro"
            )

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
                if rank <= 3:
                    classes += f" is-top-{rank}"

                with ui.element("div").classes(classes):
                    ui.label(str(rank)).classes("vault-ranking-rank")
                    with ui.element("div").classes("vault-ranking-main"):
                        with ui.row().classes(
                            "vault-ranking-title-row items-center gap-2 no-wrap"
                        ):
                            ui.label(row.display_name).classes("vault-ranking-name")
                            if row.is_current_user:
                                ui.badge("You").props("outline color=primary")

                        with ui.element("div").classes("vault-ranking-progress"):
                            ui.element("div").classes(
                                "vault-ranking-progress-fill"
                            ).style(f"width: {min(max(row.weekly_score, 0), 100):.0f}%")
                        habits = "habit" if row.active_habits == 1 else "habits"
                        ui.label(
                            f"{row.active_habits} active {habits} · {_fmt_record(row)} this week"
                        ).classes("vault-ranking-subtext")

                    with ui.element("div").classes("vault-ranking-scores"):
                        with ui.element("div").classes("vault-ranking-score-item"):
                            ui.label(_fmt_pct(row.weekly_score)).classes(
                                "vault-ranking-score-value"
                            )
                            ui.label("week score").classes("vault-ranking-score-label")
                        with ui.element("div").classes("vault-ranking-score-item"):
                            ui.label(_fmt_streak(row.avg_streak_days)).classes(
                                "vault-ranking-score-value"
                            )
                            ui.label("streak").classes("vault-ranking-score-label")
                        with ui.element("div").classes("vault-ranking-score-item"):
                            ui.label(_fmt_pct(row.completion_rate)).classes(
                                "vault-ranking-score-value"
                            )
                            ui.label("30d context").classes("vault-ranking-score-label")

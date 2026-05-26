import datetime

from beaverhabits.frontend.components import note_dialog_date_label


def test_note_dialog_date_label_uses_human_dates():
    today = datetime.date(2026, 5, 27)

    assert note_dialog_date_label(today, today) == "Today"
    assert (
        note_dialog_date_label(today, today - datetime.timedelta(days=1)) == "Yesterday"
    )
    assert (
        note_dialog_date_label(today, today + datetime.timedelta(days=1)) == "Tomorrow"
    )
    assert note_dialog_date_label(today, datetime.date(2026, 5, 1)) == "01 May 2026"

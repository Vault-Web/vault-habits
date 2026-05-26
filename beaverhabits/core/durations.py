def parse_duration_minutes(value) -> int | None:
    if value in (None, ""):
        return None

    try:
        minutes = int(float(value))
    except (TypeError, ValueError):
        return None

    return max(minutes, 0)


def format_duration(minutes: int | None) -> str:
    if not minutes:
        return ""

    hours, remaining_minutes = divmod(minutes, 60)
    if hours and remaining_minutes:
        return f"{hours}h {remaining_minutes}m"
    if hours:
        return f"{hours}h"
    return f"{remaining_minutes}m"

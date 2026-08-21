from datetime import date

import todo_app.colors as colors


def format_deadline(deadline: date | None, completed: bool) -> str:
    """Format a deadline with an urgency color and a relative hint. Strike it if completed"""
    if deadline is None:
        return "[dim]—[/dim]"

    days_left = (deadline - date.today()).days

    if days_left < 0:
        color = colors.DEADLINE_OVERDUE_COLOR
        hint = "overdue" if days_left == -1 else f"{abs(days_left)}d overdue"
    elif days_left == 0:
        color = colors.DEADLINE_TODAY_COLOR
        hint = "today"
    elif days_left <= 7:
        color = colors.DEADLINE_SOON_COLOR
        hint = f"in {days_left}d"
    else:
        color = colors.DEADLINE_OK_COLOR
        hint = f"in {days_left}d"

    striked = ""
    if completed:
        striked = "strike"

    return (
        f"[{color} {striked}]{deadline.strftime('%d-%m-%Y')}"
        f"[/{color} {striked}] [dim]({hint})[/dim]"
    )


def format_completed_mark(completed: bool) -> str:
    """Format the completed mark based on if it is completed or not"""
    if completed:
        return f"[{colors.MARK_COMPLETED_COLOR}]✓[/{colors.MARK_COMPLETED_COLOR}]"
    return f"[{colors.MARK_UNCOMPLETED_COLOR}]✗[/{colors.MARK_UNCOMPLETED_COLOR}]"


def format_created_at(created_at: date) -> str:
    """Format the created at date"""
    return created_at.strftime("%d-%m-%Y")

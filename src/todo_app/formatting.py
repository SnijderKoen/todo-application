from datetime import date

def format_deadline(deadline: date | None) -> str:
    """Format a deadline with an urgency color and a relative hint."""
    if deadline is None:
        return "[dim]—[/dim]"

    days_left = (deadline - date.today()).days

    if days_left < 0:
        color = "red"
        hint = "overdue" if days_left == -1 else f"{abs(days_left)}d overdue"
    elif days_left == 0:
        color = "yellow"
        hint = "today"
    elif days_left <= 7:
        color = "orange1"
        hint = f"in {days_left}d"
    else:
        color = "green"
        hint = f"in {days_left}d"

    return f"[{color}]{deadline.strftime('%d-%m-%Y')}[/{color}] [dim]({hint})[/dim]"
from datetime import date


def format_deadline(deadline: date | None, completed: bool) -> str:
    """Format a deadline with an urgency color and a relative hint. Strike it if completed"""
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

    striked = ""
    if completed:
        striked = "strike"

    return (
        f"[{color} {striked}]{deadline.strftime('%d-%m-%Y')}"
        f"[/{color} {striked}] [dim]({hint})[/dim]"
    )


def format_completed_mark(completed: bool) -> str:
    """Format the completed mark based on if it is completed or not"""
    completed_mark = "[green3]✓[/green3]" if completed else "[yellow]✗[/yellow]"
    return completed_mark


def format_created_at(created_at: date) -> str:
    """Format the created at date"""
    completed_at_str = (
        f"[dim light_steel_blue]{created_at.strftime('%d-%m-%Y')}[/dim light_steel_blue]"
    )
    return completed_at_str

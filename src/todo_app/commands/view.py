from datetime import date, datetime

from rich.table import Table

from tasks.storage import JSONStorage
from todo_app.console import console


def _format_deadline(deadline: date | datetime | None) -> str:
    """Format a deadline with an urgency color and a relative hint."""
    if deadline is None:
        return "[dim]—[/dim]"

    # `add` stores a `date`, but `storage.load()` reads it back as a `datetime`.
    # Normalize both to a plain `date` before doing calendar math.
    if isinstance(deadline, datetime):
        deadline = deadline.date()

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


def list_tasks() -> None:
    """Lists all tasks in a nice format and print them to the CLI"""
    storage = JSONStorage()
    storage.load()

    table = Table(title="Tasks TODO")

    table.add_column("ID", justify="left", no_wrap=True, style="bold cyan")
    table.add_column("Title", justify="left", no_wrap=False, style="bold green")
    table.add_column("Label(s)", justify="left", no_wrap=False)
    table.add_column("Completed", justify="left", no_wrap=True)
    table.add_column("Deadline", justify="left", no_wrap=True)

    for task in storage.tasks:
        label_str = ", ".join(task.labels)
        completed_mark = "[green3]✓[/green3]" if task.completed else "[yellow]✗[/yellow]"

        table.add_row(
            str(task.id),
            task.title,
            label_str,
            completed_mark,
            _format_deadline(task.deadline),
        )

    console.print(table)

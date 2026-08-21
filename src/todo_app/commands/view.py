from rich.table import Table

from tasks.storage import JSONStorage
from todo_app.console import console
from todo_app.formatting import format_completed_mark, format_created_at, format_deadline


def list_tasks() -> None:
    """Lists all tasks in a nice format and print them to the CLI"""
    storage = JSONStorage()
    storage.load()

    table = Table(title="Tasks TODO")

    table.add_column("ID", justify="left", no_wrap=True, style="bold cyan")
    table.add_column("Title", justify="left", no_wrap=False, style="bold green", overflow="fold")
    table.add_column("Label(s)", justify="left", no_wrap=False, overflow="fold")
    table.add_column("Completed", justify="left", no_wrap=True)
    table.add_column("Deadline", justify="left", no_wrap=True)
    table.add_column("Created", justify="left", no_wrap=True)

    for task in storage.tasks:
        label_str = ", ".join(task.labels) if task.labels else "[dim]—[/dim]"

        table.add_row(
            str(task.id),
            task.title,
            label_str,
            format_completed_mark(task.completed),
            format_deadline(task.deadline, task.completed),
            format_created_at(task.created),
        )

    console.print(table)

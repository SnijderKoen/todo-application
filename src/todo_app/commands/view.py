import typer

from tasks.storage import JSONStorage
from tasks.task import Task
from todo_app.console import console
from rich.table import Table
from rich.errors import NotRenderableError


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
        try:
            label_str = ""
            for label in task.labels:
                label_str += label + ", "
            label_str = label_str[:-2]

            completed_mark = ""
            if task.completed:
                completed_mark = "[green3]✓[/green3]"
            else:
                completed_mark = "[yellow]✗[/yellow]"
            table.add_row(str(task.id), task.title, label_str, completed_mark, task.deadline.strftime("%m/%d/%Y"))

        except NotRenderableError as e:
            console.print(f"[red] Render error: {e}[/red]")

    console.print(table)
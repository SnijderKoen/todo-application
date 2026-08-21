import typer

from tasks.storage import JSONStorage
from tasks.task import Task
from todo_app.console import console
from rich.table import Table


def list_tasks() -> None:
    """Lists all tasks in a nice format and print them to the CLI"""
    storage = JSONStorage()
    storage.load()

    table = Table(title="Tasks TODO")

    table.add_column("ID", justify="left", no_wrap=True, style="cyan")
    table.add_column("Title", justify="left", no_wrap=False, style="bold green")
    table.add_column("Label(s)", justify="left", no_wrap=False)
    table.add_column("Completed", justify="left", no_wrap=True)
    table.add_column("Deadline", justify="left", no_wrap=True)

    

    console.print(table)
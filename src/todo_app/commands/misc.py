import typer

from tasks.storage import JSONStorage
from todo_app.console import console


def complete_task(
    task_id: int = typer.Argument(..., help="The ID of the task to complete", metavar="TASK_ID"),
) -> None:
    "Complete a task with the given ID"
    storage = JSONStorage()
    storage.load()

    if storage.complete_task(task_id):
        console.print(
            f"[green]Completed[/green] task with ID [medium_purple1]{task_id}[/medium_purple1]"
        )
        storage.save()
    else:
        console.print(f"No task found with ID [red]{task_id}[/red].")


def uncomplete_task(
    task_id: int = typer.Argument(..., help="The ID of the task to uncomplete", metavar="TASK_ID"),
) -> None:
    """Uncomplete a task with the given ID"""
    storage = JSONStorage()
    storage.load()

    if storage.uncomplete_task(task_id):
        console.print(
            f"[orange1]Uncompleted[/orange1] "
            f"task with ID [medium_purple1]{task_id}[/medium_purple1]"
        )
        storage.save()
    else:
        console.print(f"No task found with ID [red]{task_id}[/red].")

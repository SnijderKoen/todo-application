import typer

from tasks.storage import JSONStorage
from todo_app.console import console


def delete_cmd(
    task_id: int = typer.Argument(..., help="The ID of the task to delete", metavar="TASK_ID"),
) -> None:
    """Delete a task with the given ID"""
    storage = JSONStorage()
    storage.load()

    if storage.delete_task(task_id):
        storage.save()
        console.print(f"Deleted task with ID [orange1]{task_id}[/orange1].")
    else:
        console.print(f"No task found with ID [red]{task_id}[/red].")

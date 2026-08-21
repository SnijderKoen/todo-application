import typer

import todo_app.colors as colors
from tasks.storage import JSONStorage
from todo_app.console import console


def complete_task(
    task_id: int = typer.Argument(..., help="The ID of the task to complete", metavar="TASK_ID"),
) -> None:
    """Complete a task with the given ID"""
    storage = JSONStorage()
    storage.load()

    if storage.complete_task(task_id):
        console.print(
            f"[{colors.MARK_COMPLETED_COLOR}]Completed[/{colors.MARK_COMPLETED_COLOR}] "
            f"task with ID [{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]"
        )
        storage.save()
    else:
        console.print(
            f"[{colors.NOT_FOUND_COLOR}]No task found with ID[/{colors.NOT_FOUND_COLOR}] "
            f"[{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]."
        )


def uncomplete_task(
    task_id: int = typer.Argument(..., help="The ID of the task to uncomplete", metavar="TASK_ID"),
) -> None:
    """Uncomplete a task with the given ID"""
    storage = JSONStorage()
    storage.load()

    if storage.uncomplete_task(task_id):
        console.print(
            f"[{colors.MARK_UNCOMPLETED_COLOR}]Uncompleted[/{colors.MARK_UNCOMPLETED_COLOR}] "
            f"task with ID [{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]"
        )
        storage.save()
    else:
        console.print(
            f"[{colors.NOT_FOUND_COLOR}]No task found with ID[/{colors.NOT_FOUND_COLOR}] "
            f"[{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]."
        )

import typer

import todo_app.colors as colors
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
        console.print(
            f"[{colors.DELETED_COLOR}]Deleted[/{colors.DELETED_COLOR}] task "
            f"with ID [{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]."
        )
    else:
        console.print(
            f"[{colors.NOT_FOUND_COLOR}]No task found with ID[/{colors.NOT_FOUND_COLOR}] "
            f"[{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]."
        )


def delete_label_cmd(
    args: tuple[int, str] = typer.Argument(
        ...,
        help="The ID of the task to delete the label from and the label to delete from the task",
        metavar="TASK_ID LABEL",
    ),
) -> None:
    """Delete a label from a task with the given id"""
    storage = JSONStorage()
    storage.load()
    task_id = args[0]
    label = args[1]

    remove_res = storage.delete_label(label, task_id)
    if remove_res == 0:
        storage.save()
        console.print(
            f"[{colors.DELETED_COLOR}]Deleted[/{colors.DELETED_COLOR}] label: "
            f"[{colors.LABEL_COLOR}]{label}[/{colors.LABEL_COLOR}] "
            f"from task with ID [{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]"
        )
    elif remove_res == 1:
        console.print(
            f"[{colors.NOT_FOUND_COLOR}]No task found with ID[/{colors.NOT_FOUND_COLOR}] "
            f"[{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]."
        )
    else:
        console.print(
            f"[{colors.NOT_FOUND_COLOR}]No label:[/{colors.NOT_FOUND_COLOR}] "
            f"[{colors.LABEL_COLOR}]{label}[/{colors.LABEL_COLOR}] "
            f"[{colors.NOT_FOUND_COLOR}]found for task with ID[/{colors.NOT_FOUND_COLOR}] "
            f"[{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]"
        )


def delete_deadline_cmd(
    task_id: int = typer.Argument(
        ..., help="The ID of the task to remove the deadline from", metavar="TASK_ID"
    ),
) -> None:
    """Remove the deadline fromt the task with the given ID"""
    storage = JSONStorage()
    storage.load()

    if storage.remove_deadline(task_id):
        console.print(
            f"[{colors.DELETED_COLOR}]Deleted[/{colors.DELETED_COLOR}] deadline "
            f"from task with ID [{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]"
        )
        storage.save()
    else:
        console.print(
            f"[{colors.NOT_FOUND_COLOR}]No task found with ID[/{colors.NOT_FOUND_COLOR}] "
            f"[{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]."
        )

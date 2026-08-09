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


def delete_label_cmd(args: tuple[int, str] = typer.Argument
                    (..., help="The ID of the task to delete the label from and the label to delete from the task", metavar="TASK_ID LABEL")) -> None:
    """Delete a label from a task with the given id"""
    storage = JSONStorage()
    storage.load()
    task_id = args[0]
    label = args[1]

    remove_res = storage.delete_label(label, task_id)
    if remove_res == 0:
        storage.save()
        console.print(f"Deleted label: [orange1]{label}[/orange1] from task with ID [medium_purple1]{task_id}[/medium_purple1]")
    elif remove_res == 1:
        console.print(f"No task found with ID [red]{task_id}[/red].")
    else:
        console.print(f"No label: [red]{label}[/red] found for task with ID [medium_purple1]{task_id}[/medium_purple1]")


def delete_deadline_cmd(
        task_id: int = typer.Argument(
            ...,
            help="The ID of the task to remove the deadline from",
            metavar="TASK_ID"
        ),
) -> None:
    """Remove the deadline fromt the task with the given ID"""
    storage = JSONStorage()
    storage.load()

    if storage.remove_deadline(task_id):
        console.print(f"Deleted deadline from task with ID [medium_purple1]{task_id}[/medium_purple1]")
        storage.save()
    else:
        console.print(f"No task found with ID [red]{task_id}[/red].")
   
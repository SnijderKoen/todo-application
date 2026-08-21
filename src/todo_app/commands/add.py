from datetime import datetime

import typer
import todo_app.colors as colors

from tasks.storage import JSONStorage
from tasks.task import Task
from todo_app.console import console


def add_cmd(
    title: str = typer.Argument(..., help="The title of the task", metavar="TITLE"),
    labels: list[str] = typer.Option([], "--label", "-l", help="Label(s) to add to the task"),
    deadline: str = typer.Option(None, "--deadline", "-d", help="Deadline to add to the task"),
) -> None:
    """Add a new task with the given title"""
    storage = JSONStorage()
    storage.load()

    date_obj = None
    if deadline:
        try:
            date_obj = datetime.strptime(deadline, "%d-%m-%Y").date()
        except ValueError:
            console.print(f"[{colors.ERROR_COLOR}]Please add a deadline in the format dd-mm-yyyy[/{colors.ERROR_COLOR}].")
            return

    task = Task(id=storage.next_id, title=title, labels=labels, deadline=date_obj)
    for label in labels:
        storage.labels[label] = storage.labels.get(label, 0) + 1
    storage.tasks.append(task)
    storage.next_id += 1
    storage.save()

    console.print(f"[{colors.ADDED_COLOR}]Added[/{colors.ADDED_COLOR}] task [{colors.TITLE_COLOR}]]{task.title}[/{colors.TITLE_COLOR}] with ID [{colors.ID_COLOR}]{task.id}[/{colors.ID_COLOR}].")
    for label in labels:
        console.print(f"    With label: [{colors.LABEL_COLOR}]{label}[/{colors.LABEL_COLOR}]")

    if deadline:
        console.print(f"    With deadline: [{colors.DEADLINE_COLOR}]{deadline}[/{colors.DEADLINE_COLOR}]")


def add_label_cmd(
    args: tuple[int, str] = typer.Argument(
        ...,
        help="The ID of the task to add the label to and the label to add to the task",
        metavar="TASK_ID LABEL",
    ),
) -> None:
    """Add a label to a task with given ID"""
    storage = JSONStorage()
    storage.load()
    task_id = args[0]
    label = args[1]

    if storage.add_label(label, task_id):
        console.print(
            f"[{colors.ADDED_COLOR}]Added[/{colors.ADDED_COLOR}] label: [{colors.LABEL_COLOR}]{label}[/{colors.LABEL_COLOR}] \
            to task with ID [{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]"
        )
        storage.save()
    else:
        console.print(f"[{colors.NOT_FOUND_COLOR}]No task found with ID[/{colors.NOT_FOUND_COLOR}] [{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}].")


def add_deadline_cmd(
    args: tuple[int, str] = typer.Argument(
        ...,
        help="The ID of the task and the deadline to add",
        metavar="TASK_ID DEADLINE",
    ),
) -> None:
    """Add a deadline to a task with given ID"""
    storage = JSONStorage()
    storage.load()
    task_id = args[0]
    date_str = args[1]

    try:
        date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        console.print(f"[{colors.ERROR_COLOR}]Please add a deadline in the format dd-mm-yyyy[/{colors.ERROR_COLOR}].")
        return

    if storage.add_deadline(task_id, date_obj):
        console.print(
            f"[{colors.ADDED_COLOR}]Added[/{colors.ADDED_COLOR}] deadline: [{colors.DEADLINE_COLOR}]{date_str}[/{colors.DEADLINE_COLOR}] \
            to task with ID [{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}]"
        )
        storage.save()
    else:
        console.print(f"[{colors.ERROR_COLOR}]No[/{colors.ERROR_COLOR}] task found with ID [{colors.ID_COLOR}]{task_id}[/{colors.ID_COLOR}].")

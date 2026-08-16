from datetime import datetime

import typer

from tasks.storage import JSONStorage
from tasks.task import Task
from todo_app.console import console


def add_cmd(
    title: str = typer.Argument(..., help="The title of the task", metavar="TITLE"),
    labels: list[str] = typer.Option([], "--label", "-l", help="Label(s) to add to the task"),
    deadline: str = typer.Option(None, "--deadline", "-d", help="Deadline to add to the task")
) -> None:
    """Add a new task with the given title"""
    storage = JSONStorage()
    storage.load()

    date_obj = None
    if deadline:
        try:
            date_obj = datetime.strptime(deadline, "%d-%m-%Y").date()
        except ValueError:
            console.print("[red]Please add a deadline in the format dd-mm-yyyy[/red].")
            return

    task = Task(id=storage.next_id, title=title, labels=labels, deadline=date_obj)
    storage.tasks.append(task)
    storage.next_id += 1
    storage.save()

    console.print(f"Added task [green]{task.title}[/green] with ID [cyan]{task.id}[/cyan].")


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
            f"Succesfully added label: [green1]{label}[/green1] \
            to task with ID [medium_purple1]{task_id}[/medium_purple1]"
        )
        storage.save()
    else:
        console.print(f"No task found with ID [red]{task_id}[/red].")


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
        console.print("[red]Please add a deadline in the format dd-mm-yyyy[/red].")
        return

    if storage.add_deadline(task_id, date_obj):
        console.print(
            f"Successfully added deadline: [green1]{date_str}[/green1] \
            to task with ID [medium_purple1]{task_id}[/medium_purple1]"
        )
        storage.save()
    else:
        console.print(f"No task found with ID [red]{task_id}[/red].")
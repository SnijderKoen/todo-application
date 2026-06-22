import typer

from tasks.storage import JSONStorage
from tasks.task import Task
from todo_app.console import console


def add_cmd(
    title: str = typer.Argument(..., help="The title of the task", metavar="TITLE"),
) -> None:
    """Add a new task with the given title"""
    storage = JSONStorage()
    storage.load()

    task = Task(id=storage.next_id, title=title)
    storage.tasks.append(task)
    storage.next_id += 1
    storage.save()

    console.print(f"Added task [green]{task.title}[/green] with ID [cyan]{task.id}[/cyan].")


def add_label(
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

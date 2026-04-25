from todo_app.console import console
from tasks.storage import JSONStorage
from tasks.task import Task
import typer

def add_cmd(title: str = typer.Argument
            (..., help="The title of the task", metavar="TITLE")
            ) -> None:
    """Add a new task with the given title"""
    storage = JSONStorage()
    storage.load()

    task = Task(id=storage.next_id, title=title)
    storage.tasks.append(task)
    storage.next_id += 1
    storage.save()

    console.print(f"Added task [green]{task.title}[/green] with ID [cyan]{task.id}[/cyan].")
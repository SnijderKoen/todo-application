from rich.table import Table

from tasks.storage import JSONStorage
from todo_app.console import console
from todo_app.formatting import format_completed_mark, format_created_at, format_deadline
from todo_app.colors import LABEL_COLORS


def list_tasks() -> None:
    """Lists all tasks in a nice format and print them to the CLI"""
    storage = JSONStorage()
    storage.load()

    table = Table(title="Tasks To Do")

    table.add_column("ID", justify="left", no_wrap=True, style="bold cyan", header_style="cyan")

    table.add_column(
        "Title",
        justify="left",
        no_wrap=False,
        style="thistle1",
        overflow="fold",
        header_style="thistle1",
    )

    table.add_column(
        "Label(s)", justify="left", no_wrap=False, overflow="fold", header_style="grey100"
    )

    table.add_column("Completed", justify="left", no_wrap=True, header_style="dark_sea_green3")

    table.add_column("Deadline", justify="left", no_wrap=True, header_style="red1")

    table.add_column(
        "Created",
        justify="left",
        no_wrap=True,
        style="dim light_steel_blue",
        header_style="dim light_steel_blue",
    )

    curr_color_ind = 0
    label_color_dict = {}
    for label in storage.labels.keys():
        label_color_dict[label] = LABEL_COLORS[curr_color_ind]
        curr_color_ind = (curr_color_ind + 1) % len(LABEL_COLORS)

    for task in storage.tasks:
        label_str = ""
        if task.labels:
            for label in task.labels:
                label_str += f"[{label_color_dict[label]}]{label}[/{label_color_dict[label]}], "
            label_str = label_str[:-2]
        else:
            label_str = "[dim]—[/dim]"

        table.add_row(
            str(task.id),
            task.title,
            label_str,
            format_completed_mark(task.completed),
            format_deadline(task.deadline, task.completed),
            format_created_at(task.created),
        )

    console.print(table)

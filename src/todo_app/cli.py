from __future__ import annotations

import typer
from rich.panel import Panel

from todo_app import __version__
from todo_app.commands.add import add_cmd, add_deadline_cmd, add_label_cmd
from todo_app.commands.delete import delete_cmd, delete_deadline_cmd, delete_label_cmd
from todo_app.commands.misc import complete_task, uncomplete_task
from todo_app.console import console

app = typer.Typer(
    name="todo",
    help="A local, colorful CLI todo list.",
    rich_markup_mode="rich",
    no_args_is_help=False,
    add_completion=True,
)

# Register subcommands.
app.command("add")(add_cmd)
app.command("delete")(delete_cmd)
app.command("label")(add_label_cmd)
app.command("label_del")(delete_label_cmd)
app.command("complete")(complete_task)
app.command("uncomplete")(uncomplete_task)
app.command("deadline")(add_deadline_cmd)
app.command("deadline_del")(delete_deadline_cmd)


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"todo {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """Default entry point.

    When a subcommand is invoked, Typer dispatches to it. When the user runs
    bare `todo` with no subcommand, we show the placeholder below.
    """
    if ctx.invoked_subcommand is not None:
        return

    console.print(
        Panel.fit(
            "[bold]todo[/bold] scaffold is ready.\n"
            "Run [cyan]todo --help[/cyan] to see available commands.\n"
            "Real views & subcommands arrive in the next milestone.",
            title="todo",
            border_style="cyan",
        )
    )


if __name__ == "__main__":
    app()

from typer.testing import CliRunner

from todo_app import __version__
from todo_app.cli import app

runner = CliRunner()


def test_version_flag() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_bare_invocation_shows_task_list() -> None:
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "Tasks To Do" in result.stdout


def test_help_lists_app_name() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "todo" in result.stdout.lower()

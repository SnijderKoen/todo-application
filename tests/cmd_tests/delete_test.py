"""Tests for the `todo delete` command.

These tests assume ``JSONStorage`` exposes a ``delete_task(task_id)``
method that returns ``True`` on success and ``False`` if no such task
exists.  Add it to ``tasks/storage.py`` for these tests to pass.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from todo_app.cli import app

runner = CliRunner()


@pytest.fixture
def isolated_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _seed(tmp: Path, titles: list[str]) -> None:
    """Use the `add` command itself to seed the task store, so we don't
    duplicate the JSON layout in this test file."""
    for title in titles:
        runner.invoke(app, ["add", title])


def test_delete_removes_existing_task(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha", "beta", "gamma"])

    result = runner.invoke(app, ["delete", "2"])

    assert result.exit_code == 0, result.output
    data = json.loads((isolated_cwd / "tasks.json").read_text())
    assert [t["id"] for t in data["tasks"]] == [1, 3]
    assert all(t["title"] != "beta" for t in data["tasks"])


def test_delete_prints_confirmation(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha"])

    result = runner.invoke(app, ["delete", "1"])

    assert result.exit_code == 0
    assert "1" in result.output
    assert "deleted" in result.output.lower()


def test_delete_missing_id_reports_not_found(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha"])

    result = runner.invoke(app, ["delete", "999"])

    assert result.exit_code == 0
    assert "999" in result.output
    assert "no task" in result.output.lower() or "not found" in result.output.lower()

    # The existing task must still be there.
    data = json.loads((isolated_cwd / "tasks.json").read_text())
    assert len(data["tasks"]) == 1


def test_delete_does_not_renumber_remaining_tasks(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha", "beta", "gamma"])

    runner.invoke(app, ["delete", "1"])

    data = json.loads((isolated_cwd / "tasks.json").read_text())
    # IDs are stable; deleting #1 must NOT shift #2 -> #1.
    assert [t["id"] for t in data["tasks"]] == [2, 3]
    # next_id should also keep advancing, not reuse 1.
    assert data["next_id"] == 4


def test_delete_requires_integer_id(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha"])

    result = runner.invoke(app, ["delete", "not-a-number"])

    assert result.exit_code != 0
    assert "INTEGER" in result.output or "Invalid value" in result.output


def test_delete_requires_id(isolated_cwd: Path) -> None:
    result = runner.invoke(app, ["delete"])

    assert result.exit_code != 0
    assert "TASK_ID" in result.output or "Missing argument" in result.output

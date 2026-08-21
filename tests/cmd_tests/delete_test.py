"""
Tests for the `todo delete` command.

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


# --------------------------------------------------------------------------- #
# global labels tracking (via `delete`)
# --------------------------------------------------------------------------- #


def test_delete_task_removes_global_label_count(isolated_cwd: Path) -> None:
    runner.invoke(app, ["add", "alpha", "-l", "work"])

    result = runner.invoke(app, ["delete", "1"])

    assert result.exit_code == 0, result.output
    data = json.loads((isolated_cwd / "tasks.json").read_text())
    assert data["labels"] == {}


def test_delete_one_of_two_tasks_decrements_global_count(isolated_cwd: Path) -> None:
    runner.invoke(app, ["add", "alpha", "-l", "work"])
    runner.invoke(app, ["add", "beta", "-l", "work"])

    runner.invoke(app, ["delete", "1"])

    data = json.loads((isolated_cwd / "tasks.json").read_text())
    assert data["labels"] == {"work": 1}


# --------------------------------------------------------------------------- #
# label_del command
# --------------------------------------------------------------------------- #


def test_label_del_removes_label(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha", "beta"])
    # Add two labels to task 1
    runner.invoke(app, ["label", "1", "urgent"])
    runner.invoke(app, ["label", "1", "work"])

    result = runner.invoke(app, ["label_del", "1", "urgent"])

    assert result.exit_code == 0, result.output
    data = json.loads((isolated_cwd / "tasks.json").read_text())
    assert data["tasks"][0]["labels"] == ["work"]


def test_label_del_prints_confirmation(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha"])
    runner.invoke(app, ["label", "1", "urgent"])

    result = runner.invoke(app, ["label_del", "1", "urgent"])

    assert result.exit_code == 0
    assert "urgent" in result.output
    assert "1" in result.output
    assert "Deleted" in result.output


def test_label_del_missing_task_reports_not_found(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha"])

    result = runner.invoke(app, ["label_del", "999", "urgent"])

    assert result.exit_code == 0
    assert "999" in result.output
    assert "No task" in result.output

    # The existing task must still be there.
    data = json.loads((isolated_cwd / "tasks.json").read_text())
    assert len(data["tasks"]) == 1


def test_label_del_missing_label_reports_not_found(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha"])

    result = runner.invoke(app, ["label_del", "1", "nonexistent"])

    assert result.exit_code == 0
    assert "nonexistent" in result.output
    assert "No label" in result.output

    # Task must still be there with no labels.
    data = json.loads((isolated_cwd / "tasks.json").read_text())
    assert len(data["tasks"]) == 1


def test_label_del_requires_args(isolated_cwd: Path) -> None:
    result = runner.invoke(app, ["label_del"])

    assert result.exit_code != 0
    assert "TASK_ID" in result.output and "LABEL" in result.output


def test_label_del_requires_both_args(isolated_cwd: Path) -> None:
    result = runner.invoke(app, ["label_del", "1"])

    assert result.exit_code != 0
    assert "args" in result.output


# --------------------------------------------------------------------------- #
# deadline_del command
# --------------------------------------------------------------------------- #


def test_deadline_del_removes_deadline(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha"])
    runner.invoke(app, ["deadline", "1", "31-12-2026"])

    result = runner.invoke(app, ["deadline_del", "1"])

    assert result.exit_code == 0, result.output
    data = json.loads((isolated_cwd / "tasks.json").read_text())
    assert data["tasks"][0]["deadline"] is None


def test_deadline_del_prints_confirmation(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha"])
    runner.invoke(app, ["deadline", "1", "31-12-2026"])

    result = runner.invoke(app, ["deadline_del", "1"])

    assert result.exit_code == 0
    assert "1" in result.output
    assert "Deleted" in result.output
    assert "deadline" in result.output.lower()


def test_deadline_del_missing_task_reports_not_found(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha"])

    result = runner.invoke(app, ["deadline_del", "999"])

    assert result.exit_code == 0
    assert "999" in result.output
    assert "No task" in result.output


def test_deadline_del_requires_id(isolated_cwd: Path) -> None:
    result = runner.invoke(app, ["deadline_del"])

    assert result.exit_code != 0
    assert "TASK_ID" in result.output or "Missing argument" in result.output

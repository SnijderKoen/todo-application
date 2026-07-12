"""Tests for the `todo complete` command.

These tests assume ``JSONStorage`` exposes a ``complete_task(task_id)``
method that returns ``True`` on success and ``False`` if no such task
exists.
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
    """Use the `add` command itself to seed the task store."""
    for title in titles:
        runner.invoke(app, ["add", title])


def test_complete_marks_task_completed(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha", "beta", "gamma"])

    result = runner.invoke(app, ["complete", "2"])

    assert result.exit_code == 0, result.output
    data = json.loads((isolated_cwd / "tasks.json").read_text())
    task = next(t for t in data["tasks"] if t["id"] == 2)
    assert task["completed"] is True
    assert task["completed_at"] is not None


def test_complete_prints_confirmation(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha"])

    result = runner.invoke(app, ["complete", "1"])

    assert result.exit_code == 0
    assert "1" in result.output
    assert "completed" in result.output.lower()


def test_complete_missing_id_reports_not_found(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha"])

    result = runner.invoke(app, ["complete", "999"])

    assert result.exit_code == 0
    assert "999" in result.output
    assert "no task" in result.output.lower()

    # The existing task must remain unchanged.
    data = json.loads((isolated_cwd / "tasks.json").read_text())
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["completed"] is False


def test_complete_does_not_affect_other_tasks(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha", "beta", "gamma"])

    runner.invoke(app, ["complete", "2"])

    data = json.loads((isolated_cwd / "tasks.json").read_text())
    task1 = next(t for t in data["tasks"] if t["id"] == 1)
    task3 = next(t for t in data["tasks"] if t["id"] == 3)
    assert task1["completed"] is False
    assert task3["completed"] is False


def test_complete_requires_integer_id(isolated_cwd: Path) -> None:
    _seed(isolated_cwd, ["alpha"])

    result = runner.invoke(app, ["complete", "not-a-number"])

    assert result.exit_code != 0
    assert "INTEGER" in result.output or "Invalid value" in result.output


def test_complete_requires_id(isolated_cwd: Path) -> None:
    result = runner.invoke(app, ["complete"])

    assert result.exit_code != 0
    assert "TASK_ID" in result.output or "Missing argument" in result.output
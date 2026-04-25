"""Tests for the `todo add` command.

Each test runs inside a fresh temporary working directory so that the
hardcoded ``tasks.json`` path used by the command writes into a sandbox
that pytest cleans up automatically.
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
    """Run the test with the CWD set to a fresh temp dir."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_add_creates_tasks_json(isolated_cwd: Path) -> None:
    result = runner.invoke(app, ["add", "buy milk"])

    assert result.exit_code == 0, result.output
    tasks_file = isolated_cwd / "tasks.json"
    assert tasks_file.exists()


def test_add_writes_expected_task_payload(isolated_cwd: Path) -> None:
    runner.invoke(app, ["add", "buy milk"])

    data = json.loads((isolated_cwd / "tasks.json").read_text())
    assert data["next_id"] == 2
    assert len(data["tasks"]) == 1

    task = data["tasks"][0]
    assert task["id"] == 1
    assert task["title"] == "buy milk"
    assert task["completed"] is False
    assert task["completed_at"] is None
    assert task["labels"] == []


def test_add_increments_next_id_across_invocations(isolated_cwd: Path) -> None:
    runner.invoke(app, ["add", "first"])
    runner.invoke(app, ["add", "second"])
    runner.invoke(app, ["add", "third"])

    data = json.loads((isolated_cwd / "tasks.json").read_text())
    assert [t["id"] for t in data["tasks"]] == [1, 2, 3]
    assert [t["title"] for t in data["tasks"]] == ["first", "second", "third"]
    assert data["next_id"] == 4


def test_add_prints_confirmation(isolated_cwd: Path) -> None:
    result = runner.invoke(app, ["add", "ship it"])

    assert result.exit_code == 0
    assert "ship it" in result.output
    assert "1" in result.output  # task id


def test_add_requires_title(isolated_cwd: Path) -> None:
    result = runner.invoke(app, ["add"])

    assert result.exit_code != 0
    assert "TITLE" in result.output or "Missing argument" in result.output


def test_add_help_lists_title_argument() -> None:
    result = runner.invoke(app, ["add", "--help"])

    assert result.exit_code == 0
    assert "title" in result.output.lower()

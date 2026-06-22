"""Tests for tasks.storage.JSONStorage.

All tests use pytest's built-in ``tmp_path`` fixture, which creates a fresh
temporary directory per test and removes it automatically when the test
finishes.  No manual cleanup required.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from tasks.storage import JSONStorage
from tasks.task import Task

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def make_task(
    task_id: int = 1,
    title: str = "buy milk",
    labels: list[str] | None = None,
    completed: bool = False,
    completed_at: datetime | None = None,
    created: datetime | None = None,
) -> Task:
    """Construct a Task with sensible defaults for tests."""
    return Task(
        id=task_id,
        title=title,
        labels=list(labels) if labels is not None else [],
        created=created or datetime(2026, 4, 19, 12, 0, 0),
        completed=completed,
        completed_at=completed_at,
    )


@pytest.fixture
def storage_path(tmp_path: Path) -> Path:
    """Return a path to a fresh (non-existent) tasks.json inside tmp_path."""
    return tmp_path / "tasks.json"


# --------------------------------------------------------------------------- #
# _get_dict_from_task / _get_task_from_dict
# --------------------------------------------------------------------------- #


def test_get_dict_from_task_serializes_datetime_to_iso() -> None:
    storage = JSONStorage()
    created = datetime(2026, 4, 19, 12, 30, 0)
    completed_at = datetime(2026, 4, 20, 8, 15, 0)
    task = make_task(
        task_id=7,
        title="ship it",
        labels=["work", "urgent"],
        completed=True,
        completed_at=completed_at,
        created=created,
    )

    result = storage._get_dict_from_task(task)

    assert result == {
        "id": 7,
        "title": "ship it",
        "labels": ["work", "urgent"],
        "created": created.isoformat(),
        "completed": True,
        "completed_at": completed_at.isoformat(),
    }


def test_get_dict_from_task_leaves_completed_at_none() -> None:
    storage = JSONStorage()
    task = make_task()

    result = storage._get_dict_from_task(task)

    assert result["completed"] is False
    assert result["completed_at"] is None


def test_get_task_from_dict_roundtrip() -> None:
    """Encoding then decoding should yield an equal Task."""
    storage = JSONStorage()
    original = make_task(
        task_id=3,
        title="write tests",
        labels=["dev"],
        completed=True,
        completed_at=datetime(2026, 4, 19, 15, 0, 0),
    )

    encoded = storage._get_dict_from_task(original)
    decoded = storage._get_task_from_dict(encoded)

    assert decoded == original


def test_get_task_from_dict_handles_missing_labels() -> None:
    storage = JSONStorage()
    data = {
        "id": 1,
        "title": "no labels",
        "created": datetime(2026, 4, 19).isoformat(),
        "completed": False,
        "completed_at": None,
    }

    task = storage._get_task_from_dict(data)

    assert task.labels == []


def test_get_task_from_dict_none_completed_at_stays_none() -> None:
    storage = JSONStorage()
    data = {
        "id": 1,
        "title": "pending",
        "labels": [],
        "created": datetime(2026, 4, 19).isoformat(),
        "completed": False,
        "completed_at": None,
    }

    task = storage._get_task_from_dict(data)

    assert task.completed_at is None


# --------------------------------------------------------------------------- #
# load()
# --------------------------------------------------------------------------- #


def test_load_missing_file_leaves_defaults(storage_path: Path) -> None:
    """Loading from a path that does not exist should not raise and should
    keep the storage's in-memory state at its defaults, only setting the
    filename so a subsequent save() targets the right location."""
    storage = JSONStorage()

    storage.load(str(storage_path))

    assert not storage_path.exists()
    assert storage.tasks == []
    assert storage.next_id == 1
    assert storage.version == 1
    assert str(storage.filename) == str(storage_path)


def test_load_reads_existing_file(storage_path: Path) -> None:
    payload = {
        "next_id": 5,
        "version": 1,
        "tasks": [
            {
                "id": 1,
                "title": "write report",
                "labels": ["work"],
                "created": datetime(2026, 4, 19, 9, 0, 0).isoformat(),
                "completed": False,
                "completed_at": None,
            },
            {
                "id": 4,
                "title": "ship release",
                "labels": ["work", "urgent"],
                "created": datetime(2026, 4, 18, 10, 0, 0).isoformat(),
                "completed": True,
                "completed_at": datetime(2026, 4, 19, 16, 30, 0).isoformat(),
            },
        ],
    }
    storage_path.write_text(json.dumps(payload))

    storage = JSONStorage()
    storage.load(str(storage_path))

    assert storage.next_id == 5
    assert storage.version == 1
    assert len(storage.tasks) == 2

    first, second = storage.tasks
    assert first.id == 1
    assert first.title == "write report"
    assert first.labels == ["work"]
    assert first.completed is False
    assert first.completed_at is None
    assert first.created == datetime(2026, 4, 19, 9, 0, 0)

    assert second.id == 4
    assert second.completed is True
    assert second.completed_at == datetime(2026, 4, 19, 16, 30, 0)


def test_load_empty_task_list(storage_path: Path) -> None:
    storage_path.write_text(json.dumps({"next_id": 1, "version": 1, "tasks": []}))
    storage = JSONStorage()

    storage.load(str(storage_path))

    assert storage.tasks == []
    assert storage.next_id == 1


# --------------------------------------------------------------------------- #
# save()
# --------------------------------------------------------------------------- #


def test_save_writes_expected_json_structure(storage_path: Path) -> None:
    storage = JSONStorage(
        filename=storage_path,
        next_id=3,
        version=1,
        tasks=[
            make_task(task_id=1, title="alpha"),
            make_task(task_id=2, title="beta", labels=["home"]),
        ],
    )

    storage.save()

    data = json.loads(storage_path.read_text())
    assert data["next_id"] == 3
    assert data["version"] == 1
    assert len(data["tasks"]) == 2
    assert data["tasks"][0]["title"] == "alpha"
    assert data["tasks"][1]["labels"] == ["home"]


def test_save_removes_tmp_file(storage_path: Path) -> None:
    """The atomic write should leave only the final file, not the .tmp one."""
    storage = JSONStorage(filename=storage_path, tasks=[make_task()])

    storage.save()

    assert storage_path.exists()
    assert not storage_path.with_suffix(".tmp").exists()


def test_save_then_load_roundtrip(storage_path: Path) -> None:
    """Writing via save() and reading back via load() preserves all data."""
    tasks = [
        make_task(task_id=1, title="first", labels=["a"]),
        make_task(
            task_id=2,
            title="second",
            labels=["b", "c"],
            completed=True,
            completed_at=datetime(2026, 4, 19, 18, 0, 0),
        ),
    ]
    writer = JSONStorage(filename=storage_path, next_id=3, version=1, tasks=list(tasks))
    writer.save()

    reader = JSONStorage()
    reader.load(str(storage_path))

    assert reader.next_id == 3
    assert reader.version == 1
    assert reader.tasks == tasks


def test_save_overwrites_existing_file(storage_path: Path) -> None:
    storage_path.write_text(json.dumps({"next_id": 99, "version": 1, "tasks": []}))

    storage = JSONStorage(
        filename=storage_path,
        next_id=2,
        version=1,
        tasks=[make_task(task_id=1, title="only one")],
    )
    storage.save()

    data = json.loads(storage_path.read_text())
    assert data["next_id"] == 2
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["title"] == "only one"


# --------------------------------------------------------------------------- #
# add_label()
# --------------------------------------------------------------------------- #


def test_add_label(storage_path: Path) -> None:
    task = make_task(task_id=3, title="task", labels=[])
    storage = JSONStorage(filename=storage_path, next_id=4, version=69, tasks=[task])
    label_added = storage.add_label("label", 3)
    storage.save()

    data = json.loads(storage_path.read_text())
    assert label_added 
    assert data["next_id"] == 4
    assert data["tasks"][0]["labels"] == ["label"]


def test_add_label_task_doesnot_exist(storage_path: Path) -> None:
    task = make_task(task_id=3, title="task", labels=[])
    storage = JSONStorage(filename=storage_path, next_id=4, version=69, tasks=[task])
    label_added = storage.add_label("label", 4)
    storage.save()

    data = json.loads(storage_path.read_text())
    assert not label_added
    assert data["next_id"] == 4
    assert data["tasks"][0]["title"] == "task"
    assert data["tasks"][0]["labels"] == []


# --------------------------------------------------------------------------- #
# delete_label()
# --------------------------------------------------------------------------- #


def test_delete_label(storage_path: Path) -> None:
    task = make_task(task_id=3, title="task", labels=["label", "other"])
    storage = JSONStorage(filename=storage_path, next_id=4, version=69, tasks=[task])
    result = storage.delete_label("label", 3)
    storage.save()

    data = json.loads(storage_path.read_text())
    assert result == 0
    assert data["next_id"] == 4
    assert data["tasks"][0]["labels"] == ["other"]


def test_delete_label_task_doesnot_exist(storage_path: Path) -> None:
    task = make_task(task_id=3, title="task", labels=["label"])
    storage = JSONStorage(filename=storage_path, next_id=4, version=69, tasks=[task])
    result = storage.delete_label("label", 4)
    storage.save()

    data = json.loads(storage_path.read_text())
    assert result == 1
    assert data["next_id"] == 4
    assert data["tasks"][0]["labels"] == ["label"]


def test_delete_label_label_doesnot_exist(storage_path: Path) -> None:
    task = make_task(task_id=3, title="task", labels=["label"])
    storage = JSONStorage(filename=storage_path, next_id=4, version=69, tasks=[task])
    result = storage.delete_label("nonexistent", 3)
    storage.save()

    data = json.loads(storage_path.read_text())
    assert result == 2
    assert data["next_id"] == 4
    assert data["tasks"][0]["labels"] == ["label"]

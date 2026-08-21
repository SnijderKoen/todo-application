import json
import os
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

from tasks.task import Task


def _to_date(value: str) -> date:
    """Parse an ISO date string, ignoring any time-of-day/timezone suffix."""
    return date.fromisoformat(value.split("T")[0])


def default_tasks_file() -> Path:
    """Return the default location for the task data file.

    Uses an explicit ``TODO_TASKS_FILE`` override when set (e.g. in tests),
    otherwise the XDG data directory, so the app keeps a single list no
    matter which directory it's run from.
    """
    override = os.environ.get("TODO_TASKS_FILE")
    if override:
        return Path(override).expanduser()

    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    data_home = Path(xdg_data_home) if xdg_data_home else Path.home() / ".local" / "share"
    return data_home / "todo-app" / "tasks.json"


@dataclass
class JSONStorage:
    filename: Path = Path()
    next_id: int = 1
    version: int = 1
    auto_remove_days: int = 10
    tasks: list[Task] = field(default_factory=list)
    labels: dict[str, int] = field(default_factory=dict)

    def _get_task_from_dict(self, data: dict) -> Task:
        """Convert a dictionary to a Task instance"""
        return Task(
            id=data["id"],
            title=data["title"],
            labels=list(data.get("labels", [])),
            created=_to_date(data["created"]),
            completed=data["completed"],
            completed_at=_to_date(data["completed_at"]) if data["completed_at"] else None,
            deadline=_to_date(data["deadline"]) if data["deadline"] is not None else None,
        )

    def _get_dict_from_task(self, task: Task) -> dict:
        """Convert a Task instance to a dictionary"""
        data_dict = asdict(task)
        data_dict["created"] = task.created.isoformat()
        data_dict["completed_at"] = task.completed_at.isoformat() if task.completed_at else None
        data_dict["deadline"] = task.deadline.isoformat() if task.deadline is not None else None
        return data_dict

    def load(self, filename: str | Path | None = None) -> None:
        """
        Load tasks from the JSON storage file if it exists
        After loading, remove tasks completed longer ago than auto_remove_days
        """
        task_file = Path(filename) if filename is not None else default_tasks_file()
        if not task_file.exists():
            self.filename = task_file
            return
        else:
            data = json.loads(task_file.read_text())
            self.filename = task_file
            self.next_id = data["next_id"]
            self.version = data["version"]
            self.tasks = [self._get_task_from_dict(task) for task in data["tasks"]]
            labels = data.get("labels", {})
            if isinstance(labels, list):
                labels = {item["label"]: item["count"] for item in labels}
            self.labels = labels

            today = date.today()
            for task in self.tasks[:]:
                if (
                    task.completed
                    and task.completed_at is not None
                    and (today - task.completed_at).days > self.auto_remove_days
                ):
                    self.delete_task(task.id)

    def save(self) -> None:
        """Save tasks to the JSON storage file"""
        data = {
            "next_id": self.next_id,
            "version": self.version,
            "labels": self.labels,
            "tasks": [self._get_dict_from_task(task) for task in self.tasks],
        }
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        json_tmp = self.filename.with_suffix(".tmp")
        json_tmp.write_text(json.dumps(data, indent=2))
        os.replace(json_tmp, self.filename)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID
        Returns True if deleted, False if the task was not found
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                for label in task.labels:
                    if label in self.labels:
                        self.labels[label] -= 1
                        if self.labels[label] <= 0:
                            del self.labels[label]

                del self.tasks[i]
                return True
        return False

    def add_label(self, label: str, task_id: int) -> bool:
        """
        Add a label to a task by its ID
        Returns True if label was added, False if the task was not found
        """
        lower_label = label.lower()

        for task in self.tasks:
            if task.id == task_id:
                task.add_label(lower_label)
                self.labels[lower_label] = self.labels.get(lower_label, 0) + 1
                return True
        return False

    def delete_label(self, label: str, task_id: int) -> int:
        """
        Remove a label from a task by its ID
        Returns 0 if label was removed, 1 if the task was not found, 2 if the label was not found
        """
        lower_label = label.lower()
        status = 1
        for task in self.tasks:
            if task.id == task_id:
                status = task.delete_label(lower_label)
                if status == 0 and lower_label in self.labels:
                    self.labels[lower_label] -= 1
                    if self.labels[lower_label] <= 0:
                        del self.labels[lower_label]

        return status

    def complete_task(self, task_id: int) -> bool:
        """
        Complete a task if it exists and return True
        If the task does not exist, return False
        """
        for task in self.tasks:
            if task.id == task_id:
                task.complete_task()
                return True

        return False

    def uncomplete_task(self, task_id: int) -> bool:
        """
        Uncomplete a task if it exists and return True
        If the task does not exist, return False
        """
        for task in self.tasks:
            if task.id == task_id:
                task.uncomplete_task()
                return True

        return False

    def add_deadline(self, task_id: int, deadline: date) -> bool:
        """
        Add a deadline to a task with task_id and return True
        If the task does not exist, return False
        """
        for task in self.tasks:
            if task.id == task_id:
                task.add_deadline(deadline)
                return True

        return False

    def remove_deadline(self, task_id: int) -> bool:
        """
        Remove a deadline from a task with task_id and return True
        If the task does not exist, return False
        """
        for task in self.tasks:
            if task.id == task_id:
                task.remove_deadline()
                return True

        return False

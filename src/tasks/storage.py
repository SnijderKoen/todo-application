import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from tasks.task import Task


@dataclass
class JSONStorage:
    filename: Path = Path()
    next_id: int = 1
    version: int = 1
    tasks: list[Task] = field(default_factory=list)

    def _get_task_from_dict(self, data: dict) -> Task:
        """Convert a dictionary to a Task instance"""
        return Task(
            id=data["id"],
            title=data["title"],
            labels=list(data.get("labels", [])),
            created=datetime.fromisoformat(data["created"]),
            completed=data["completed"],
            completed_at=datetime.fromisoformat(data["completed_at"])
            if data["completed_at"]
            else None,
        )

    def _get_dict_from_task(self, task: Task) -> dict:
        """Convert a Task instance to a dictionary"""
        data_dict = asdict(task)
        data_dict["created"] = task.created.isoformat()
        data_dict["completed_at"] = task.completed_at.isoformat() if task.completed_at else None
        return data_dict

    def load(self, filename: str = "tasks.json") -> None:
        """Load tasks from the JSON storage file if it exists"""
        task_file = Path(filename)
        if not task_file.exists():
            self.filename = Path(filename)
            return
        else:
            data = json.loads(task_file.read_text())
            self.filename = Path(filename)
            self.next_id = data["next_id"]
            self.version = data["version"]
            self.tasks = [self._get_task_from_dict(task) for task in data["tasks"]]

    def save(self) -> None:
        """Save tasks to the JSON storage file"""
        data = {
            "next_id": self.next_id,
            "version": self.version,
            "tasks": [self._get_dict_from_task(task) for task in self.tasks],
        }
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
                del self.tasks[i]
                return True
        return False

    def add_label(self, label: str, task_id: int) -> bool:
        """
        Add a label to a task by its ID
        Returns True if label was added, False if the task was not found
        """
        for task in self.tasks:
            if task.id == task_id:
                task.add_label(label)
                return True
        return False
    
    def delete_label(self, label: str, task_id: int) -> int:
        """
        Remove a label from a task by its ID
        Returns 0 if label was removed, 1 if the task was not found, 2 if the label was not found
        """
        status = 1
        for task in self.tasks:
            if task.id == task_id:
                status = task.delete_label(label)

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
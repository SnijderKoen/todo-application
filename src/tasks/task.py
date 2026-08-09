from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass
class Task:
    id: int
    title: str
    labels: list[str] = field(default_factory=list)
    created: datetime = field(default_factory=datetime.now)
    completed: bool = False
    completed_at: datetime | None = None
    deadline: datetime | None = None


    def add_label(self, label: str) -> None:
        """Add a label to the task"""
        self.labels.append(label)


    def delete_label(self, label: str) -> int:
        """
        Remove a label if it exists
        Return 0 if the label was removed, 2 if the label wasn't found
        """
        for j, lab in enumerate(self.labels):
            if lab == label:
                del self.labels[j]
                return 0
            
        return 2
    

    def complete_task(self) -> None:
        """Complete a task at the current time"""
        self.completed = True
        self.completed_at = datetime.now(ZoneInfo("Europe/Amsterdam"))


    def uncomplete_task(self) -> None:
        """Uncomplete a task and reset completed at"""
        self.completed = False
        self.completed_at = None


    def add_deadline(self, deadline: datetime) -> None:
        """Add a deadline to a task"""
        self.deadline = deadline


    def remove_deadline(self) -> None:
        """Remove a deadline from a task"""
        self.deadline = None
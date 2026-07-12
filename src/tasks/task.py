from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    id: int
    title: str
    labels: list[str] = field(default_factory=list)
    created: datetime = field(default_factory=datetime.now)
    completed: bool = False
    completed_at: datetime | None = None


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

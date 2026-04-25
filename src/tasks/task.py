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

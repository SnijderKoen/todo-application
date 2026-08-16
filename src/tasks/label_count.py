from dataclasses import dataclass

@dataclass
class LabelCount:
    label: str
    count: int = 1

    def get_label(self) -> str:
        return self.label

    def get_count(self) -> int:
        return self.count

    def increment_count(self):
        self.count += 1

    def decrement_count(self):
        self.count -= 1

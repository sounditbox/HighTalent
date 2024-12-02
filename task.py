from dataclasses import dataclass

from priority import Priority


@dataclass
class Task:
    id: int
    title: str
    description: str
    category: str
    due_date: str
    priority: Priority
    status: str = "Не выполнена"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority.value,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Task(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=Priority(data["priority"]),
            status=data.get("status", "Не выполнена")
        )

    def __str__(self):
        return f"{self.id} | {self.title}\n" + \
            f"{self.description}\n" + \
            f"📋: {self.category}\n" + \
            f"📅: {self.due_date}\n" + \
            f"⚡: {self.priority}\n" + \
            f"✅: {self.status}\n"

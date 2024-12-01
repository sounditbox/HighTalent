import json
import os
from task import Task


class TaskManager:
    next_id = 0

    def __init__(self, filename: str = 'tasks.json'):
        self.filename = filename
        self.tasks: list[Task] = self.load_tasks()

    def load_tasks(self) -> list[Task]:
        if not os.path.exists(self.filename):
            self.save_tasks()
        with open(self.filename, 'r', encoding='utf-8') as file:
            tasks = json.load(file)
            if tasks:
                TaskManager.next_id = max(map(lambda t: t['id'], tasks))
                return [Task.from_dict(task) for task in tasks]
        return []

    def save_tasks(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in self.tasks], file,
                      ensure_ascii=False, indent=4)

    def add_task(self, title, description, category, due_date, priority) -> Task:
        TaskManager.next_id += 1  # Автоинкремент
        task = Task(TaskManager.next_id, title, description, category, due_date,
                    priority)
        self.tasks.append(task)
        self.save_tasks()
        return task

    def edit_task(self, task_id, **kwargs) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            for key, value in kwargs.items():
                setattr(task, key, value)
            self.save_tasks()
            return True
        return False

    def delete_task(self, task_id) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False

    def get_task_by_id(self, task_id) -> Task:
        return next((task for task in self.tasks if task.id == task_id), None)

    def search_tasks(self, keyword=None, category=None, status=None) -> list[Task]:
        results = self.tasks
        if keyword:
            results = [task for task in results if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]
        if category:
            results = [task for task in results if task.category == category]
        if status:
            results = [task for task in results if task.status == status]
        return results

    def mark_task_completed(self, task_id) -> bool:
        return self.edit_task(task_id, status="Выполнена")

    def get_tasks(self, **kwargs) -> list[Task]:
        if 'category' in kwargs:
            return [task for task in self.tasks if task.category == kwargs['category']]
        return []

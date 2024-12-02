import json
import os

from exceptions import TaskNotFound
from task import Task


class TaskManager:
    next_id = 0

    def __init__(self, filename: str = 'tasks.json'):
        """
        Initializes the TaskManager with a specific filename for storing tasks.

        Args:
            filename (str): The name of the file where tasks are stored. Defaults to 'tasks.json'.
        """
        self.filename = filename
        self.tasks: list[Task] = self._load_tasks()

    def _load_tasks(self) -> list[Task]:
        """
        Loads tasks from a JSON file specified by the filename attribute.
        If the file does not exist, it creates an empty task file.
        Updates the TaskManager's next_id to the highest ID found in the file.

        Returns:
            list[Task]: A list of Task objects loaded from the file.
        """
        if not os.path.exists(self.filename):
            self._save_tasks()
        with open(self.filename, 'r', encoding='utf-8') as file:
            tasks = json.load(file)
            if tasks:
                TaskManager.next_id = max(tasks, key=lambda t: t['id'])['id']
                return [Task.from_dict(task) for task in tasks]
        return []

    def _save_tasks(self) -> None:
        """
        Saves the current list of tasks to the JSON file specified by the filename attribute.
        The tasks are serialized to a list of dictionaries, using each task's to_dict method.
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in self.tasks], file,
                      ensure_ascii=False, indent=4)

    def get_tasks(self) -> list[Task]:
        """
        Returns the current list of tasks.

        Returns:
            list[Task]: A list of Task objects.
        """
        return self.tasks

    def add_task(self, title, description, category, due_date, priority) -> Task:
        """
        Adds a new task to the task list and saves it.

        Args:
            title (str): The title of the task.
            description (str): The description of the task.
            category (str): The category of the task.
            due_date (str): The due date of the task.
            priority (str): The priority level of the task.

        Returns:
            Task: The newly created Task object.
        """
        TaskManager.next_id += 1
        task = Task(TaskManager.next_id, title, description, category, due_date,
                    priority)
        self.tasks.append(task)
        self._save_tasks()
        return task

    def edit_task(self, task_id, **kwargs) -> bool:
        """
        Edits an existing task with given attributes and saves the changes.

        Args:
            task_id (int): The ID of the task to edit.
            **kwargs: Arbitrary keyword arguments for task attributes to update.

        Returns:
            bool: True if the task was successfully edited.

        Raises:
            TaskNotFound: If the task with the specified ID is not found.
        """
        task = self.get_task_by_id(task_id)
        if not task:
            raise TaskNotFound
        for key, value in kwargs.items():
            setattr(task, key, value)
        self._save_tasks()
        return True

    def delete_task(self, task_id) -> bool:
        """
        Deletes a task by its ID and saves the change.

        Args:
            task_id (int): The ID of the task to delete.

        Returns:
            bool: True if the task was successfully deleted.

        Raises:
            TaskNotFound: If the task with the specified ID is not found.
        """
        task = self.get_task_by_id(task_id)
        if not task:
            raise TaskNotFound
        self.tasks.remove(task)
        self._save_tasks()
        return True

    def get_task_by_id(self, task_id) -> Task:
        """
        Retrieves a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            Task: The Task object with the specified ID, or None if not found.
        """
        return next((task for task in self.tasks if task.id == task_id), None)

    def search_tasks(self, keyword=None, category=None, status=None) -> list[Task]:
        """
        Searches for tasks based on keyword, category, or status.

        Args:
            keyword (str, optional): A keyword to search in the task title or description.
            category (str, optional): The category to filter tasks by.
            status (str, optional): The status to filter tasks by.

        Returns:
            list[Task]: A list of Task objects that match the search criteria.
        """
        results = self.tasks
        if keyword:
            results = [task for task in results if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]
        if category:
            results = [task for task in results if task.category == category]
        if status:
            results = [task for task in results if task.status == status]
        return results

    def complete_task(self, task_id) -> bool:
        """
        Marks a task as completed by setting its status to "Выполнена".

        Args:
            task_id (int): The ID of the task to mark as completed.

        Returns:
            bool: True if the task was successfully marked as completed.
        """
        return self.edit_task(task_id, status="Выполнена")

    def get_tasks_by(self, **kwargs) -> list[Task]:
        """
        Retrieves tasks filtered by specified attributes.

        Args:
            **kwargs: Arbitrary keyword arguments for task attributes to filter by.

        Returns:
            list[Task]: A list of Task objects that match the specified attributes.
        """
        if 'category' in kwargs:
            return [task for task in self.tasks if task.category == kwargs['category']]
        return []

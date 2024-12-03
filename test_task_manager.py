import tempfile
import time
import unittest
import os
from task import Task
from task_manager import TaskManager
from priority import Priority
from exceptions import TaskNotFound, InvalidPriority, InvalidDate
from constants import DATE_FORMAT

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary file
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_filename = self.temp_file.name
        self.temp_file.close()

        # Reset next_id before each test
        TaskManager.next_id = 0

        # Create TaskManager instance
        self.task_manager = TaskManager(filename=self.test_filename)

    def tearDown(self):
        # Delete the TaskManager instance
        del self.task_manager

        # Remove the temporary file
        os.unlink(self.test_filename)

    def test_add_task(self):
        task = self.task_manager.add_task(
            title="Тестовая задача",
            description="Это тестовая задача.",
            category="Тестирование",
            due_date="2023-12-31",
            priority=Priority.HIGH.value
        )
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Тестовая задача")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(len(self.task_manager.tasks), 1)

    def test_add_task_invalid_priority(self):
        with self.assertRaises(InvalidPriority):
            self.task_manager.add_task(
                title="Задача с недопустимым приоритетом",
                description="Эта задача имеет недопустимый приоритет.",
                category="Тестирование",
                due_date="2023-12-31",
                priority="НедопустимыйПриоритет"
            )

    def test_add_task_invalid_due_date(self):
        with self.assertRaises(InvalidDate):
            self.task_manager.add_task(
                title="Задача с недопустимой датой",
                description="Эта задача имеет недопустимую дату.",
                category="Тестирование",
                due_date="31-12-2023",  # Неправильный формат
                priority=Priority.HIGH.value
            )

    def test_get_task_by_id(self):
        task = self.task_manager.add_task(
            title="Получить задачу",
            description="Получить эту задачу по ID.",
            category="Тестирование",
            due_date="2023-12-31",
            priority=Priority.MEDIUM.value
        )
        retrieved_task = self.task_manager.get_task_by_id(task.id)
        self.assertEqual(retrieved_task, task)

    def test_get_task_by_invalid_id(self):
        retrieved_task = self.task_manager.get_task_by_id(999)
        self.assertIsNone(retrieved_task)

    def test_edit_task(self):
        task = self.task_manager.add_task(
            title="Редактировать задачу",
            description="Эта задача будет отредактирована.",
            category="Тестирование",
            due_date="2023-12-31",
            priority=Priority.LOW.value
        )
        self.task_manager.edit_task(task.id, title="Отредактированная задача", priority=Priority.HIGH)
        edited_task = self.task_manager.get_task_by_id(task.id)
        self.assertEqual(edited_task.title, "Отредактированная задача")
        self.assertEqual(edited_task.priority, Priority.HIGH)

    def test_edit_task_invalid_id(self):
        with self.assertRaises(TaskNotFound):
            self.task_manager.edit_task(999, title="Должно завершиться ошибкой")

    def test_delete_task(self):
        task = self.task_manager.add_task(
            title="Удалить задачу",
            description="Эта задача будет удалена.",
            category="Тестирование",
            due_date="2023-12-31",
            priority=Priority.MEDIUM.value
        )
        self.task_manager.delete_task(task.id)
        self.assertIsNone(self.task_manager.get_task_by_id(task.id))
        self.assertEqual(len(self.task_manager.tasks), 0)

    def test_delete_task_invalid_id(self):
        with self.assertRaises(TaskNotFound):
            self.task_manager.delete_task(999)

    def test_complete_task(self):
        task = self.task_manager.add_task(
            title="Завершить задачу",
            description="Эта задача будет завершена.",
            category="Тестирование",
            due_date="2023-12-31",
            priority=Priority.LOW.value
        )
        self.task_manager.complete_task(task.id)
        completed_task = self.task_manager.get_task_by_id(task.id)
        self.assertEqual(completed_task.status, "Выполнена")

    def test_find_task_by_keyword(self):
        task1 = self.task_manager.add_task(
            title="Задача с ключевым словом 1",
            description="Первая задача с ключевым словом.",
            category="Тестирование",
            due_date="2023-12-31",
            priority=Priority.HIGH.value
        )
        task2 = self.task_manager.add_task(
            title="Другая задача",
            description="Вторая задача без ключевого слова.",
            category="Тестирование",
            due_date="2023-12-31",
            priority=Priority.LOW.value
        )
        results = self.task_manager.find_task(keyword="ключевым")
        self.assertIn(task1, results)
        self.assertNotIn(task2, results)

    def test_find_task_by_category(self):
        task1 = self.task_manager.add_task(
            title="Задача категории 1",
            description="Первая задача в категории.",
            category="Работа",
            due_date="2023-12-31",
            priority=Priority.MEDIUM.value
        )
        task2 = self.task_manager.add_task(
            title="Задача категории 2",
            description="Вторая задача в категории.",
            category="Личное",
            due_date="2023-12-31",
            priority=Priority.LOW.value
        )
        results = self.task_manager.find_task(category="Работа")
        self.assertIn(task1, results)
        self.assertNotIn(task2, results)

    def test_find_task_by_status(self):
        task1 = self.task_manager.add_task(
            title="Задача со статусом 1",
            description="Первая задача со статусом.",
            category="Тестирование",
            due_date="2023-12-31",
            priority=Priority.HIGH.value
        )
        self.task_manager.complete_task(task1.id)
        task2 = self.task_manager.add_task(
            title="Задача со статусом 2",
            description="Вторая задача без статуса.",
            category="Тестирование",
            due_date="2023-12-31",
            priority=Priority.LOW.value
        )
        results = self.task_manager.find_task(status="Выполнена")
        self.assertIn(task1, results)
        self.assertNotIn(task2, results)

    def test_get_tasks_by_category(self):
        task1 = self.task_manager.add_task(
            title="Задача по работе",
            description="Задача в категории Работа.",
            category="Работа",
            due_date="2023-12-31",
            priority=Priority.HIGH.value
        )
        task2 = self.task_manager.add_task(
            title="Личная задача",
            description="Задача в категории Личное.",
            category="Личное",
            due_date="2023-12-31",
            priority=Priority.MEDIUM.value
        )
        work_tasks = self.task_manager.get_tasks_by(category="Работа")
        self.assertIn(task1, work_tasks)
        self.assertNotIn(task2, work_tasks)

    def test_task_to_dict(self):
        task = Task(
            id=1,
            title="Задача в словарь",
            description="Преобразовать эту задачу в словарь.",
            category="Тестирование",
            due_date="2023-12-31",
            priority=Priority.HIGH
        )
        task_dict = task.to_dict()
        expected_dict = {
            "id": 1,
            "title": "Задача в словарь",
            "description": "Преобразовать эту задачу в словарь.",
            "category": "Тестирование",
            "due_date": "2023-12-31",
            "priority": Priority.HIGH.value,
            "status": "Не выполнена"
        }
        self.assertEqual(task_dict, expected_dict)

    def test_task_from_dict(self):
        task_dict = {
            "id": 1,
            "title": "Задача из словаря",
            "description": "Преобразовать этот словарь в задачу.",
            "category": "Тестирование",
            "due_date": "2023-12-31",
            "priority": Priority.HIGH.value,
            "status": "Не выполнена"
        }
        task = Task.from_dict(task_dict)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Задача из словаря")
        self.assertEqual(task.priority, Priority.HIGH)

    def test_save_and_load_tasks(self):
        # Add a task and save it
        task = self.task_manager.add_task(
            title="Сохранить задачу",
            description="Эта задача будет сохранена.",
            category="Тестирование",
            due_date="2023-12-31",
            priority=Priority.HIGH.value
        )
        # Ensure the tasks are saved to the file
        self.task_manager._save_tasks()

        # Create a new TaskManager instance to load tasks
        new_task_manager = TaskManager(filename=self.test_filename)
        self.assertEqual(len(new_task_manager.tasks), 1)
        loaded_task = new_task_manager.get_task_by_id(task.id)
        self.assertEqual(loaded_task.title, "Сохранить задачу")
        # Clean up
        del new_task_manager


if __name__ == '__main__':
    unittest.main()

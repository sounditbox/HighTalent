import datetime
import os

from task_manager import TaskManager


class IOHandler:
    def __init__(self, tm: TaskManager):
        self.tm = tm

    def get_tasks(self, **kwargs):
        tasks = self.tm.get_tasks(**kwargs)
        if not tasks:
            print("Задачи не найдены.")
            return
        for task in tasks:
            print(task)

    def get_cat_tasks(self):
        cat = input('Введите категорию')
        self.get_tasks(category=cat)

    def add_task(self):
        try:
            title = input("Введите название: ")
            description = input("Введите описание: ")
            category = input("Введите категорию: ")
            due_date = input("Введите срок выполнения (ГГГГ-ММ-ДД): ")
            datetime.datetime.strptime(due_date, '%Y-%m-%d')  # Проверка даты
            priority = input("Введите приоритет (Низкий, Средний, Высокий): ")
            if priority not in ["Низкий", "Средний", "Высокий"]:
                raise ValueError("Неверный приоритет")
            self.tm.add_task(title, description, category, due_date, priority)
            print("Задача добавлена успешно.")
        except Exception as e:
            print(f"Ошибка при добавлении задачи: {e}")

    @staticmethod
    def clear():
        os.system('cls') if os.name == 'nt' else os.system('clear')

    def edit_task(self):
        try:
            task_id = int(input("Введите ID задачи для редактирования: "))
            task = self.tm.get_task_by_id(task_id)
            if not task:
                print("Задача не найдена.")
                return
            title = input(
                f"Введите новое название ({task.title}): ") or task.title
            description = input(
                f"Введите новое описание ({task.description}): ") or task.description
            category = input(
                f"Введите новую категорию ({task.category}): ") or task.category
            due_date = input(
                f"Введите новый срок выполнения ({task.due_date}): ") or task.due_date
            priority = input(
                f"Введите новый приоритет ({task.priority}): ") or task.priority
            self.tm.edit_task(task_id, title=title, description=description,
                              category=category, due_date=due_date,
                              priority=priority)
            print(f"Задача {task_id} обновлена успешно.")
        except Exception as e:
            print(f"Ошибка при редактировании задачи: {e}")

    def complete_task(self):
        try:
            task_id = int(
                input("Введите ID задачи для отметки как выполненной: "))
            if self.tm.mark_task_completed(task_id):
                print("Задача отмечена как выполненная.")
            else:
                print("Задача не найдена.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def delete_task(self):
        try:
            task_id = int(input("Введите ID задачи для удаления: "))
            if self.tm.delete_task(task_id):
                print("Задача удалена.")
            else:
                print("Задача не найдена.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def find_task(self):
        keyword = input(
            "Введите ключевое слово для поиска (или оставьте пустым): ")
        category = input("Введите категорию для поиска (или оставьте пустым): ")
        status = input(
            "Введите статус для поиска (Выполнена/Не выполнена или оставьте пустым): ")
        tasks = self.tm.search_tasks(keyword=keyword or None,
                                     category=category or None,
                                     status=status or None)
        # ???
        self.get_tasks(tasks)

    def exit(self):
        print('Пока-пока')
        self.tm.save_tasks()
        exit()

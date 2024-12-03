import os

from colorama import Style, Fore

from constants import DELIMITER, BASE_EXCEPTION_MESSAGE, COMMAND_PALETTE, \
    ERROR_PALETTE
from exceptions import TaskManagerException
from task import Task
from task_manager import TaskManager


class IOHandler:
    tm: TaskManager = TaskManager()

    def get_tasks(self):
        tasks = self.tm.get_tasks()
        self.print_(tasks)

    def get_cat_tasks(self):
        cat = input('Введите категорию:\n')
        tasks = self.tm.get_tasks_by(category=cat)
        self.print_(tasks)

    def add_task(self, **kwargs):
        if not kwargs:
            title = input("Введите название: ")
            description = input("Введите описание: ")
            category = input("Введите категорию: ")
            due_date = input("Введите срок выполнения (ГГГГ-ММ-ДД): ")
            priority = input("Введите приоритет (Низкий, Средний, Высокий): ")
        else:
            title = kwargs.get('title')
            description = kwargs.get('description')
            category = kwargs.get('category')
            due_date = kwargs.get('due_date')
            priority = kwargs.get('priority')
        try:
            self.tm.add_task(title, description, category, due_date, priority)
        except TaskManagerException as e:
            print(BASE_EXCEPTION_MESSAGE, e)
        else:
            print("Задача добавлена успешно.")

    def edit_task(self, **kwargs):
        if not kwargs:
            task_id = int(input("Введите ID задачи для редактирования: "))
            task = self.tm.get_task_by_id(task_id)
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
        else:
            task_id = kwargs.get('id')
            title = kwargs.get('title')
            description = kwargs.get('description')
            category = kwargs.get('category')
            due_date = kwargs.get('due_date')
            priority = kwargs.get('priority')
        try:
            self.tm.edit_task(task_id, title=title, description=description,
                              category=category, due_date=due_date,
                              priority=priority)
        except TaskManagerException as e:
            print(BASE_EXCEPTION_MESSAGE, e)
        else:
            print(f"Задача {task_id} обновлена успешно.")

    def complete_task(self, task_id=None):
        if not task_id:
            task_id = int(input("Введите ID задачи:\n"))
        try:
            self.tm.complete_task(task_id)
        except TaskManagerException as e:
            print("Ошибка выполнения задачи:", e)
        else:
            print("Задача отмечена как выполненная.")

    def delete_task(self, t_id=None):
        if not t_id:
            t_id = int(input("Введите ID задачи для удаления: "))
        try:
            self.tm.delete_task(t_id)
        except TaskManagerException as e:
            print(BASE_EXCEPTION_MESSAGE, e)
        else:
            print("Задача удалена.")

    def find_task(self):
        keyword = input(
            "Введите ключевое слово для поиска (или оставьте пустым): ")
        category = input("Введите категорию для поиска (или оставьте пустым): ")
        status = input(
            "Введите статус для поиска (Выполнена/Не выполнена или оставьте пустым): ")
        tasks = self.tm.find_task(keyword=keyword or None,
                                  category=category or None,
                                  status=status or None)
        self.print_(tasks)

    def interactive(self):
        actions = {
            1: ('Все задачи', self.get_tasks),
            2: ('Задачи по категории', self.get_cat_tasks),
            3: ('Добавить задачу', self.add_task),
            4: ('Редактировать задачу', self.edit_task),
            5: ('Выполнить задачу', self.complete_task),
            6: ('Удалить задачу', self.delete_task),
            7: ('Поиск задач', self.find_task),
            0: ('Выход', self.exit),
        }

        self.clear()
        while True:
            print(Fore.YELLOW + "\nМенеджер задач")
            for act in actions:
                print(f'{act}. {actions[act][0]}')
            print(Fore.RESET)

            action = int(input("Выберите действие:\n"))
            self.clear()

            if action in actions:
                description, func = actions[action]
                print(COMMAND_PALETTE + f'Действие: {description}')
                print(Fore.RESET)
                func()
            else:
                print(Fore.RED + "Не понял тебя. Попробуй снова.")
                print(Style.RESET_ALL)

    def get_tasks_by(self, category):
        self.tm.get_tasks_by(category=category)

    @staticmethod
    def clear():
        os.system('cls') if os.name == 'nt' else os.system('clear')

    @staticmethod
    def exit():
        print('Пока-пока')
        exit()

    @staticmethod
    def print_(tasks: list[Task]):
        if not tasks:
            print(ERROR_PALETTE + 'Задачи не найдены.')

        print(DELIMITER)
        for task in tasks:
            print(task)
            print(DELIMITER)
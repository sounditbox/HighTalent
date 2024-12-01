from iohandler import IOHandler
from task_manager import TaskManager

manager = TaskManager('tasks.json')
display = IOHandler(manager)
actions = {
    1: ('Все задачи', display.get_tasks),
    2: ('Задачи по категории', display.get_cat_tasks),
    3: ('Добавить задачу', display.add_task),
    4: ('Редактировать задачу', display.edit_task),
    5: ('Выполнить задачу', display.complete_task),
    6: ('Удалить задачу', display.delete_task),
    7: ('Поиск задач', display.find_task),
    0: ('Выход', display.exit),
}


def main():
    display.clear()
    while True:
        print("\nМенеджер задач")
        for act in actions:
            print(act, actions[act][0], sep='. ')

        action = input("Выберите действие: ")
        display.clear()

        if action in actions:
            description, func = actions[int(action)]
            print(f'Действие: {description}')
            func()
        else:
            print("Не понял тебя. Попробуй снова.")


if __name__ == "__main__":
    main()

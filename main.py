from iohandler import IOHandler
from colorama import Style, Fore


def main():
    display = IOHandler()

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

    display.clear()
    while True:
        print(Fore.YELLOW + "\nМенеджер задач")
        for act in actions:
            print(f'{act}. {actions[act][0]}')
        print(Fore.RESET)

        action = int(input("Выберите действие:\n"))
        display.clear()

        if action in actions:
            description, func = actions[action]
            print(Fore.GREEN + f'Действие: {description}')
            print(Fore.RESET)
            func()
        else:
            print(Fore.RED + "Не понял тебя. Попробуй снова.")
            print(Style.RESET_ALL)


if __name__ == "__main__":
    main()

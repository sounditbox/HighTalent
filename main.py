import argparse

from iohandler import IOHandler
from priority import Priority
from task_manager import TaskManager

task_manager = TaskManager()

parser = argparse.ArgumentParser(description='Менеджер задач')
subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

# Команда для добавления задачи
p_add = subparsers.add_parser('add', help='Добавить новую задачу')
p_add.add_argument('--title',
                   required=True, help='Название задачи')
p_add.add_argument('--description',
                   required=True, help='Описание задачи')

p_add.add_argument('--category',
                   required=True, help='Категория задачи')
p_add.add_argument('--due_date',
                   required=True, help='Срок выполнения (ГГГГ-ММ-ДД)')
p_add.add_argument('--priority', required=True,
                   choices=Priority.list(), help='Приоритет задачи')

# Команда для просмотра задач
p_list = subparsers.add_parser('list', help='Просмотр задач')
p_list.add_argument('--category',
                    help='Категория для отображения задач')

# Команда для редактирования задачи
p_edit = subparsers.add_parser('edit', help='Редактировать задачу')
p_edit.add_argument('--id', required=True, type=int,
                    help='ID задачи для редактирования')
p_edit.add_argument('--title', help='Новое название задачи')
p_edit.add_argument('--description', help='Новое описание задачи')
p_edit.add_argument('--category', help='Новая категория задачи')
p_edit.add_argument('--due_date',
                    help='Новый срок выполнения (ГГГГ-ММ-ДД)')
p_edit.add_argument('--priority', help='Новый приоритет задачи',
                    choices=Priority.list())

# Команда для отметки задачи как выполненной
p_complete = subparsers.add_parser('complete',
                                   help='Отметить задачу как выполненную')
p_complete.add_argument('--id', required=True, type=int,
                        help='ID задачи для отметки как выполненной')

# Команда для удаления задачи
p_delete = subparsers.add_parser('delete', help='Удалить задачу')
p_delete.add_argument('--id', type=int, help='ID задачи для удаления')
p_delete.add_argument('--category', help='Категория задач для удаления')

# Команда для поиска задач
p_search = subparsers.add_parser('search', help='Поиск задач')
p_search.add_argument('--keyword', help='Ключевое слово для поиска')
p_search.add_argument('--category', help='Категория для поиска')
p_search.add_argument('--status', choices=['Выполнена', 'Не выполнена'],
                      help='Статус задачи для поиска')

# Команда для интерактивного режима
p_interactive = subparsers.add_parser('it',
                                      help='Режим интерактивного взаимодействия')
args = parser.parse_args()

display = IOHandler()

match args.command:
    case 'it':
        display.interactive()
    case 'add':
        display.add_task(**vars(args))
    case 'list':
        if args.category:
            tasks = display.get_tasks_by(category=args.category)
        else:
            tasks = display.get_tasks()
    case 'edit':
        data = {
            'id': args.id,
            'title': args.title,
            'description': args.description,
            'category': args.category,
            'due_date': args.due_date,
            'priority': args.priority
        }
        display.edit_task(**data)
    case 'complete':
        display.complete_task(args.id)
    case 'delete':
        display.delete_task(args.id)
    case 'search':
        display.find_task(**args)
    case _:
        parser.print_help()

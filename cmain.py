import argparse

from settings import DELIMITER
from task_manager import TaskManager

task_manager = TaskManager()

parser = argparse.ArgumentParser(description='Менеджер задач')
subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

# Команда для добавления задачи
p_add = subparsers.add_parser('add', help='Добавить новую задачу')
p_add.add_argument(
    '--title',
    required=True, help='Название задачи'
)
p_add.add_argument(
    '--description',
    required=True, help='Описание задачи')

p_add.add_argument(
    '--category',
    required=True, help='Категория задачи'
)
p_add.add_argument(
    '--due_date',
    required=True, help='Срок выполнения (ГГГГ-ММ-ДД)'
)
p_add.add_argument(
    '--priority', required=True,
    choices=['Низкий', 'Средний', 'Высокий'],
    help='Приоритет задачи'
)

# Команда для просмотра задач
p_list = subparsers.add_parser('list', help='Просмотр задач')
p_list.add_argument(
    '--category',
    help='Категория для отображения задач'
)

# Команда для редактирования задачи
p_edit = subparsers.add_parser('edit', help='Редактировать задачу')
p_edit.add_argument(
    '--id',
    required=True, type=int, help='ID задачи для редактирования'
)
p_edit.add_argument(
    '--title',
    help='Новое название задачи'
)
p_edit.add_argument(
    '--description',
    help='Новое описание задачи'
)
p_edit.add_argument(
    '--category',
    help='Новая категория задачи'
)
p_edit.add_argument(
    '--due_date',
    help='Новый срок выполнения (ГГГГ-ММ-ДД)'
)
p_edit.add_argument(
    '--priority',
    help='Новый приоритет задачи', choices=['Низкий', 'Средний', 'Высокий']
)

# Команда для отметки задачи как выполненной
p_complete = subparsers.add_parser('complete',
                                   help='Отметить задачу как выполненную')
p_complete.add_argument(
    '--id',
    required=True, type=int, help='ID задачи для отметки как выполненной')

# Команда для удаления задачи
p_delete = subparsers.add_parser('delete', help='Удалить задачу')
p_delete.add_argument(
    '--id',
    type=int, help='ID задачи для удаления')
p_delete.add_argument(
    '--category',
    help='Категория задач для удаления')

# Команда для поиска задач
p_search = subparsers.add_parser('search', help='Поиск задач')
p_search.add_argument(
    '--keyword',
    help='Ключевое слово для поиска')
p_search.add_argument(
    '--category',
    help='Категория для поиска')
p_search.add_argument(
    '--status',
    choices=['Выполнена', 'Не выполнена'],
    help='Статус задачи для поиска')

args = parser.parse_args()

if args.command == 'add':
    task_manager.add_task(args.title, args.description, args.category,
                          args.due_date, args.priority)
elif args.command == 'list':
    if args.category:
        tasks = task_manager.get_tasks_by_cat(category=args.category)
    else:
        tasks = task_manager.get_tasks()

    print(DELIMITER)
    print((DELIMITER + '\n').join(str(t) for t in tasks))
    print(DELIMITER)
elif args.command == 'edit':
    data = {
        'title': args.title,
        'description': args.description,
        'category': args.category,
        'due_date': args.due_date,
        'priority': args.priority
    }
    task_manager.edit_task(args.id, **data)
elif args.command == 'complete':
    task_manager.complete_task(args.id)
elif args.command == 'delete':
    task_manager.delete_task(args.id)
elif args.command == 'search':
    task_manager.search_tasks(**args)
else:
    parser.print_help()

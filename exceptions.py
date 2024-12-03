class TaskManagerException(Exception):
    pass


class TaskNotFound(TaskManagerException):
    message = 'Задача не найдена'


class TaskAlreadyCompleted(TaskManagerException):
    message = 'Задача уже выполнена'


class InvalidPriority(TaskManagerException):
    message = 'Неверная приоритетность задачи'


class InvalidDate(TaskManagerException):
    pass

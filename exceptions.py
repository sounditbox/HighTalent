class TaskManagerException(Exception):
    pass


class TaskNotFound(TaskManagerException):
    message = 'Задача не найдена'


class DateTimeException(TaskManagerException):
    pass


class InvalidDate(DateTimeException):
    pass

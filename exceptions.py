class TaskManagerException(Exception):
    pass


class TaskNotFound(TaskManagerException):
    message = 'Задача не найдена'

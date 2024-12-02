import enum


class Priority(enum.Enum):
    LOW = 'Низкий'
    MEDIUM = 'Средний'
    HIGH = 'Высокий'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

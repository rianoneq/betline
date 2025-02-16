from dataclasses import dataclass


@dataclass(eq=False)
class BaseDomainException(Exception):
    @property
    def message(self):
        return "Базовая ошибка"


@dataclass(eq=False)
class BaseEventException(BaseDomainException):
    @property
    def message(self):
        return "Базовая ошибка эвента"


@dataclass(eq=False)
class EventNotFoundException(BaseDomainException):
    @property
    def message(self):
        return 'Такого события не существует.'


@dataclass(eq=False)
class EventAlreadyExistsException(BaseDomainException):
    @property
    def message(self):
        return 'Такое событие уже существует.'


@dataclass(eq=False)
class EventStateAlreadyChangedException(BaseDomainException):
    @property
    def message(self):
        return 'Статус этого события уже был изменен.'


@dataclass(eq=False)
class EventDeadlineInPastException(BaseDomainException):
    @property
    def message(self):
        return 'Дедлайн этого события должен быть в будущем (UTC).'

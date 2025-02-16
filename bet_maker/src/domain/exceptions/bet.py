from dataclasses import dataclass


@dataclass(eq=False)
class BaseDomainException(Exception):
    @property
    def message(self):
        return "Базовая ошибка"


@dataclass(eq=False)
class BaseBetException(BaseDomainException):
    @property
    def message(self):
        return "Базовая ошибка ставки"


@dataclass(eq=False)
class BetNotFoundException(BaseDomainException):
    @property
    def message(self):
        return "Такой bet не существует."


@dataclass(eq=False)
class BetAlreadyExistsException(BaseDomainException):
    @property
    def message(self):
        return "Такая bet уже существует."

from dataclasses import dataclass
from uuid import UUID


@dataclass(eq=False)
class EventNotFoundException(Exception):
    @property
    def message(self):
        return "Событие на которые вы пытаетесь сделать ставку не существует."


@dataclass(eq=False)
class EventCompletedException(Exception):
    @property
    def message(self):
        return "Событие на которые вы пытаетесь сделать ставку уже завершено."


@dataclass(eq=False)
class EventDeadlineInPastException(Exception):
    @property
    def message(self):
        return "Событие на которые вы пытаетесь сделать ставку истекло."


@dataclass(eq=False)
class CannotCompleteNotFoundEventException(Exception):
    event_id: UUID

    @property
    def message(self):
        return f"Нельзя завершить несуществующее событие {self.event_id}."


@dataclass(eq=False)
class EventAlreadyExistsException(Exception):
    event_id: UUID

    @property
    def message(self):
        return f"Такое событие уже существует {self.event_id}."

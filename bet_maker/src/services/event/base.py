from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from domain.entities.event import Event


class BaseEventService(ABC):
    @abstractmethod
    async def check_avaiblity_to_bet(self, event_id: UUID) -> None:
        ...

    @abstractmethod
    async def create(self, event: Event) -> Event:
        ...

    @abstractmethod
    async def mark_completed(self, event_id: UUID) -> None:
        ...

from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from domain.entities.event import (
    Event,
    EventState,
)


class BaseEventService(ABC):
    @abstractmethod
    async def get_event(self, event_id: UUID) -> Event:
        ...

    @abstractmethod
    async def create(self, event: Event) -> None:
        ...

    @abstractmethod
    async def get_event_list(self) -> list[Event]:
        ...

    @abstractmethod
    async def update(
        self, event_id: UUID, state: EventState,
    ) -> list[Event]:
        ...

    @abstractmethod
    async def handle_new_bet(
        self, event_id: UUID, bet_amount: float,
    ) -> list[Event]:
        ...

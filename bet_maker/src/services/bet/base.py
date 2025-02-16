from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from domain.entities.bet import Bet
from domain.entities.event import EventState


class BaseBetService(ABC):
    @abstractmethod
    async def get_by_bet_id(self, bet_id: UUID) -> Bet | None:
        ...

    @abstractmethod
    async def create(self, bet: Bet) -> Bet:
        ...

    @abstractmethod
    async def get_bet_list(self) -> list[Bet]:
        ...

    @abstractmethod
    async def change_bets_states(self, event_id: UUID, event_state: EventState) -> None:
        ...

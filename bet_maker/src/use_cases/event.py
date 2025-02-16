from dataclasses import dataclass

from domain.commands.event import (
    EventCreatedCommand,
    EventEndedCommand,
)
from domain.entities.event import Event
from services.bet.base import BaseBetService
from services.event.base import BaseEventService


@dataclass
class EventEndedUseCase:
    bet_service: BaseBetService
    event_service: BaseEventService

    async def execute(self, command: EventEndedCommand) -> None:
        await self.event_service.mark_completed(event_id=command.event_id)
        await self.bet_service.change_bets_states(
            event_id=command.event_id,
            event_state=command.event_state,
        )


@dataclass
class EventCreatedUseCase:
    event_service: BaseEventService

    async def execute(self, command: EventCreatedCommand) -> None:
        return await self.event_service.create(
            Event(
                event_id=command.event_id,
                event_deadline=command.event_deadline,
                completed=False,
            ),
        )

from dataclasses import dataclass

from domain.commands.bet import NewBetCommand
from infra.message_broker.base import BaseMessageBroker
from services.base import BaseEventService


@dataclass
class BetCreatedUseCase:
    event_service: BaseEventService
    message_broker: BaseMessageBroker

    async def execute(self, command: NewBetCommand) -> None:
        await self.event_service.handle_new_bet(
            bet_amount=command.bet_amount,
            event_id=command.event_id,
        )

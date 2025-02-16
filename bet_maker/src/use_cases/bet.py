from dataclasses import dataclass

import orjson

from core.configs import settings
from domain.commands.bet import (
    CreateBetCommand,
    GetBetCommand,
)
from domain.entities.bet import Bet
from domain.messages.bets import NewBetCreatedMessage
from infra.message_broker.base import BaseMessageBroker
from services.bet.base import BaseBetService
from services.event.base import BaseEventService


@dataclass
class CreateBetUseCase:
    bet_service: BaseBetService
    event_service: BaseEventService
    message_broker: BaseMessageBroker

    async def execute(self, command: CreateBetCommand) -> Bet:
        await self.event_service.check_avaiblity_to_bet(event_id=command.bet.event_id, bet_amount=command.bet.amount)
        bet = await self.bet_service.create(command.bet)
        await self.message_broker.send_message(
            topic=settings.new_bet_topic,
            key=str(bet.bet_id).encode(),
            value=orjson.dumps(
                NewBetCreatedMessage(
                    bet_amount=float(bet.amount),
                    event_id=str(bet.event_id),
                )
            ),
        )

        return bet


@dataclass
class GetBetUseCase:
    bet_service: BaseBetService

    async def execute(self, command: GetBetCommand) -> Bet:
        return await self.bet_service.get_bet(command.bet_id)


@dataclass
class GetBetListUseCase:
    bet_service: BaseBetService

    async def execute(self) -> list[Bet]:
        return await self.bet_service.get_bet_list()

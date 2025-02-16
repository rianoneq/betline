from dataclasses import dataclass

import orjson

from core.configs import settings
from domain.commands.event import (
    CreateEventCommand,
    GetEventCommand,
    UpdateEventCommand,
)
from domain.entities.event import Event
from domain.messages.event import (
    EventStateChangedMessage,
    NewEventCreatedMessage,
)
from infra.message_broker.base import BaseMessageBroker
from services.base import BaseEventService


@dataclass
class CreateEventUseCase:
    event_service: BaseEventService
    message_broker: BaseMessageBroker

    async def execute(self, command: CreateEventCommand) -> Event:
        event = await self.event_service.create(event=command.event)
        await self.message_broker.send_message(
            topic=settings.new_event_topic,
            key=str(event.event_id).encode(),
            value=orjson.dumps(
                NewEventCreatedMessage(
                    event_deadline=event.deadline,
                    event_id=str(event.event_id),
                )
            ),
        )

        return event


@dataclass
class UpdateEventUseCase:
    event_service: BaseEventService
    message_broker: BaseMessageBroker

    async def execute(self, command: UpdateEventCommand) -> Event:
        event = await self.event_service.update(
            event_id=command.event_id,
            state=command.state,
        )
        await self.message_broker.send_message(
            topic=settings.event_change_topic,
            key=str(event.event_id).encode(),
            value=orjson.dumps(
                EventStateChangedMessage(
                    event_state=event.state,
                    event_id=str(event.event_id),
                )
            ),
        )

        return event


@dataclass
class GetEventUseCase:
    event_service: BaseEventService

    async def execute(self, command: GetEventCommand) -> Event:
        return await self.event_service.get_event(event_id=command.event_id)


@dataclass
class GetEventListUseCase:
    event_service: BaseEventService

    async def execute(self) -> list[Event]:
        return await self.event_service.get_event_list()

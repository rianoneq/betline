from dataclasses import (
    asdict,
    dataclass,
)
from datetime import datetime
from uuid import UUID

import pytz
from sqlalchemy import (
    select,
    update,
)

from domain.entities.event import Event
from domain.exceptions.event import (
    CannotCompleteNotFoundEventException,
    EventAlreadyExistsException,
    EventCompletedException,
    EventDeadlineInPastException,
    EventNotFoundException,
)
from gateways.postgresql.database import Database
from gateways.postgresql.models.event import EventORM
from services.event.base import BaseEventService


@dataclass
class ORMEventService(BaseEventService):
    database: Database

    async def get_event(self, event_id: UUID) -> Event:
        stmt = select(EventORM).where(EventORM.event_id == event_id).limit(1)
        async with self.database.get_read_only_session() as session:
            orm_event = await session.scalar(stmt)
            if not orm_event:
                return None
            return orm_event.to_entity()

    async def mark_completed(self, event_id: UUID) -> None:
        event = await self.get_event(event_id)
        if not event:
            raise CannotCompleteNotFoundEventException(event_id=event_id)

        event.completed = True
        async with self.database.get_session() as session:
            await session.execute(update(EventORM), [asdict(event)])

    async def check_avaiblity_to_bet(self, event_id: UUID) -> None:
        event = await self.get_event(event_id)
        if not event:
            raise EventNotFoundException()

        if event.completed:
            raise EventCompletedException()

        if event.event_deadline < datetime.now(tz=pytz.UTC):
            raise EventDeadlineInPastException()

    async def create(self, event: Event) -> Event:
        if await self.get_event(event.event_id):
            raise EventAlreadyExistsException(event_id=event.event_id)

        orm_event = EventORM.from_entity(event)
        async with self.database.get_session() as session:
            session.add(orm_event)

        return orm_event.to_entity()

    async def get_or_create(self, event: Event) -> Event:
        orm_event = await self.get_event(event.event_id)
        if not orm_event:
            orm_event = await self.create(event)

        return orm_event

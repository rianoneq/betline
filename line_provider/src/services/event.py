
from dataclasses import (
    asdict,
    dataclass,
)
from datetime import datetime
from decimal import Decimal
from uuid import UUID

import pytz
from gateways.postgresql.database import Database
from gateways.postgresql.models.event import EventORM
from sqlalchemy import (
    select,
    update,
)

from domain.entities.event import (
    Event,
    EventState,
)
from domain.exceptions import (
    EventAlreadyExistsException,
    EventDeadlineInPastException,
    EventNotFoundException,
    EventStateAlreadyChangedException,
)
from services.base import BaseEventService


@dataclass
class ORMEventService(BaseEventService):
    database: Database

    async def get_by_event_id(self, event_id: UUID) -> Event | None:
        stmt = select(EventORM).where(EventORM.event_id == event_id).limit(1)
        async with self.database.get_read_only_session() as session:
            event_orm = await session.scalar(stmt)
            if not event_orm:
                return None
            return event_orm.to_entity()

    async def create(self, event: Event) -> Event:
        if await self.get_by_event_id(event.event_id):
            raise EventAlreadyExistsException()

        if event.deadline < datetime.now(tz=pytz.UTC):
            raise EventDeadlineInPastException()

        orm_event = EventORM.from_entity(event)
        async with self.database.get_session() as session:
            session.add(orm_event)

        return orm_event.to_entity()

    async def get_or_create(self, event: Event) -> Event:
        db_event = await self.get_by_event_id(event.event_id)
        if db_event:
            return db_event
        return await self.create(event)

    async def update(self, event_id: UUID, state: EventState) -> Event:
        event = await self.get_event(event_id)
        if not event:
            raise EventNotFoundException()

        if event.state != EventState.NEW:
            raise EventStateAlreadyChangedException()

        event.state = state
        async with self.database.get_session() as session:
            await session.execute(update(EventORM), [asdict(event)])

        return event

    async def get_event(self, event_id: UUID) -> Event:
        event = await self.get_by_event_id(event_id=event_id)

        if not event:
            raise EventNotFoundException()

        return event

    async def get_event_list(self) -> list[Event]:
        stmt = select(EventORM).where(EventORM.deadline > datetime.now())
        async with self.database.get_read_only_session() as session:
            events_orm = await session.execute(stmt)
            return [event_orm.to_entity() for event_orm, *_ in events_orm]

    async def handle_new_bet(self, event_id: UUID, bet_amount: float) -> None:
        event = await self.get_by_event_id(event_id=event_id)
        if not event:
            raise EventNotFoundException()

        event.coefficient = Decimal(max(float(event.coefficient) - bet_amount * 0.1, 1))
        async with self.database.get_session() as session:
            await session.execute(update(EventORM), [asdict(event)])

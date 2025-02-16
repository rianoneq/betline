from datetime import datetime
from uuid import (
    UUID,
    uuid4,
)

from sqlalchemy import DateTime
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from domain.entities.event import Event
from gateways.postgresql.models.base import BaseORM


class EventORM(BaseORM):
    event_id: Mapped[UUID] = mapped_column(primary_key=True, unique=True, default=uuid4)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)

    __tablename__ = "events"

    def to_entity(self) -> Event:
        return Event(
            event_id=self.event_id,
            event_deadline=self.deadline,
            completed=self.completed,
        )

    @staticmethod
    def from_entity(event: Event) -> 'EventORM':
        return EventORM(
            event_id=event.event_id,
            deadline=event.event_deadline,
            completed=event.completed,
        )

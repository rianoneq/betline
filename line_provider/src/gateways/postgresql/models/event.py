from datetime import datetime
from decimal import Decimal
from uuid import (
    UUID,
    uuid4,
)

from gateways.postgresql.models.base import BaseORM
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    Numeric,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from core.configs import settings
from domain.entities.event import (
    Event,
    EventState,
)


class EventORM(BaseORM):
    event_id: Mapped[UUID] = mapped_column(primary_key=True, unique=True, default=uuid4)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    coefficient: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=settings.base_event_coefficient
    )
    state = mapped_column(Enum(EventState), nullable=False, default=EventState.NEW.value)

    __tablename__ = 'events'
    __table_args__ = (
        CheckConstraint(
            'coefficient >= 1', name='check_coefficient_positive'
        ),
    )

    def to_entity(self) -> Event:
        return Event(
            event_id=self.event_id,
            deadline=self.deadline,
            coefficient=self.coefficient,
            state=self.state,
        )

    @staticmethod
    def from_entity(event: Event) -> 'EventORM':
        return EventORM(
            event_id=event.event_id,
            deadline=event.deadline,
            coefficient=Decimal(event.coefficient),
            state=event.state,
        )

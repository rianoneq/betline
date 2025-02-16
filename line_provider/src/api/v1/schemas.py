from datetime import datetime
from decimal import Decimal
from typing import (
    Any,
    Generic,
    TypeVar,
)
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)

from core.configs import settings
from domain.entities.event import (
    Event,
    EventState,
)


TData = TypeVar('TData')
TListItem = TypeVar('TListItem')


class PaginationOutSchema(BaseModel):
    ...


class ListPaginatedResponse(BaseModel, Generic[TListItem]):
    items: list[TListItem]
    pagination: PaginationOutSchema


class ApiResponse(BaseModel, Generic[TData]):
    data: TData | dict | list = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[Any] = Field(default_factory=list)


class EventOutSchema(BaseModel):
    coefficient: float
    deadline: datetime
    event_id: UUID
    state: EventState

    @staticmethod
    def from_entity(entity: Event) -> 'EventOutSchema':
        return EventOutSchema(
            event_id=entity.event_id,
            coefficient=Decimal(entity.coefficient),
            deadline=entity.deadline,
            state=entity.state,
        )


class CreateEventInSchema(BaseModel):
    deadline: datetime

    def to_entity(self, event_id: UUID):
        return Event(
            event_id=event_id,
            coefficient=settings.base_event_coefficient,
            deadline=self.deadline,
            state=settings.base_event_state,
        )


class UpdateEventInSchema(BaseModel):
    state: EventState


class ErrorSchema(BaseModel):
    message: str

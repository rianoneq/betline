from dataclasses import dataclass
from uuid import UUID

from domain.entities.event import (
    Event,
    EventState,
)


@dataclass
class GetEventListCommand:
    search: str


@dataclass
class GetEventCommand:
    event_id: UUID


@dataclass
class CreateEventCommand:
    event: Event


@dataclass
class GetOrCreateCommand:
    event: Event


@dataclass
class UpdateEventCommand:
    event_id: UUID
    state: EventState

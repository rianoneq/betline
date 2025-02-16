from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.entities.event import EventState


@dataclass
class EventEndedCommand:
    event_state: EventState
    event_id: UUID


@dataclass
class EventCreatedCommand:
    event_deadline: datetime
    event_id: UUID

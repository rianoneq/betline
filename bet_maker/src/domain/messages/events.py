from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from domain.entities.event import EventState
from domain.messages.base import BaseMessage


@dataclass
class EventStateChangedMessage(BaseMessage):
    message_title: ClassVar[str] = 'Event State Changed'

    event_state: EventState
    event_id: UUID

from datetime import datetime
from uuid import UUID

from domain.commands.event import (
    EventCreatedCommand,
    EventEndedCommand,
)
from domain.entities.event import EventState


def convert_event_changed_message_to_command(message: dict) -> EventEndedCommand:
    return EventEndedCommand(
        event_id=UUID(message["event_id"]),
        event_state=EventState(message["event_state"]),
    )


def convert_new_event_message_to_command(message: dict) -> EventCreatedCommand:
    return EventCreatedCommand(
        event_id=UUID(message["event_id"]),
        event_deadline=datetime.fromisoformat(
            message["event_deadline"].replace("Z", "+00:00")
        ),
    )

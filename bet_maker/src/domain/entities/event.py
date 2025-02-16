from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class EventState(int, Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


@dataclass
class Event:
    event_id: UUID
    event_deadline: datetime
    completed: bool

import datetime
import uuid
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class EventState(int, Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


@dataclass
class Event:
    event_id: uuid.UUID
    coefficient: Decimal
    deadline: datetime
    state: EventState

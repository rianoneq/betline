from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from uuid import UUID


class BetState(int, Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


@dataclass
class Bet:
    event_id: UUID
    bet_id: UUID
    amount: Decimal
    state: BetState

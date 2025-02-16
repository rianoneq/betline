from dataclasses import dataclass
from uuid import UUID


@dataclass
class NewBetCommand:
    bet_amount: float
    event_id: UUID

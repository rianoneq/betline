from dataclasses import dataclass
from uuid import UUID

from domain.entities.bet import Bet


@dataclass
class GetBetListCommand:
    search: str


@dataclass
class GetBetCommand:
    bet_id: UUID


@dataclass
class CreateBetCommand:
    bet: Bet

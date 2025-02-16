from dataclasses import dataclass
from decimal import Decimal
from typing import ClassVar
from uuid import UUID

from domain.messages.base import BaseMessage


@dataclass
class NewBetCreatedMessage(BaseMessage):
    message_title: ClassVar[str] = "New Bet Created"

    bet_amount: Decimal
    event_id: UUID

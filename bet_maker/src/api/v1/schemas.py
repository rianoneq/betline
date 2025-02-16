from decimal import Decimal
from typing import (
    Any,
    Generic,
    TypeVar,
)
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)

from core.configs import settings
from domain.entities.bet import (
    Bet,
    BetState,
)


TData = TypeVar('TData')


class ApiResponse(BaseModel, Generic[TData]):
    data: TData | dict | list = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[Any] = Field(default_factory=list)


class BetOutSchema(BaseModel):
    amount: float
    bet_id: UUID
    event_id: UUID
    state: BetState

    @staticmethod
    def from_entity(entity: Bet) -> 'BetOutSchema':
        return BetOutSchema(
            event_id=entity.event_id,
            amount=entity.amount,
            bet_id=entity.bet_id,
            state=entity.state,
        )


class CreateBetInSchema(BaseModel):
    amount: float
    event_id: UUID

    def to_entity(self, bet_id: UUID) -> Bet:
        return Bet(
            event_id=self.event_id,
            amount=Decimal(round(self.amount, 2)),
            bet_id=bet_id,
            state=settings.base_bet_state,
        )


class ErrorSchema(BaseModel):
    message: str

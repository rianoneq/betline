from decimal import Decimal
from uuid import (
    UUID,
    uuid4,
)

from sqlalchemy import (
    CheckConstraint,
    Enum,
    Numeric,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from domain.entities.bet import (
    Bet,
    BetState,
)
from gateways.postgresql.models.base import BaseORM


class BetORM(BaseORM):
    bet_id: Mapped[UUID] = mapped_column(primary_key=True, unique=True, default=uuid4)
    event_id: Mapped[UUID] = mapped_column(nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    state = mapped_column(Enum(BetState), nullable=False, default=BetState.NEW.value)

    __tablename__ = 'bets'
    __table_args__ = (
        CheckConstraint("amount > 0", name="check_amount_positive"),
    )

    def to_entity(self) -> Bet:
        return Bet(
            event_id=self.event_id,
            bet_id=self.bet_id,
            amount=self.amount,
            state=self.state,
        )

    @staticmethod
    def from_entity(bet: Bet) -> 'BetORM':
        return BetORM(
            event_id=bet.event_id,
            bet_id=bet.bet_id,
            amount=bet.amount,
            state=bet.state,
        )

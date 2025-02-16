
from dataclasses import (
    asdict,
    dataclass,
)
from uuid import UUID

from sqlalchemy import (
    select,
    update,
)

from domain.entities.bet import (
    Bet,
    BetState,
)
from domain.exceptions.bet import (
    BetAlreadyExistsException,
    BetNotFoundException,
)
from gateways.postgresql.database import Database
from gateways.postgresql.models.bet import BetORM
from services.bet.base import BaseBetService


@dataclass
class ORMBetService(BaseBetService):
    database: Database

    async def get_by_bet_id(self, bet_id: UUID) -> Bet | None:
        stmt = select(BetORM).where(BetORM.bet_id == bet_id).limit(1)
        async with self.database.get_read_only_session() as session:
            orm_bet = await session.scalar(stmt)
            if not orm_bet:
                return None
            return orm_bet.to_entity()

    async def create(self, bet: Bet) -> Bet:
        if await self.get_by_bet_id(bet.bet_id):
            raise BetAlreadyExistsException()

        orm_bet = BetORM.from_entity(bet)
        async with self.database.get_session() as session:
            session.add(orm_bet)

        return orm_bet.to_entity()

    async def batch_bets_update(self, bets: list[Bet]):
        async with self.database.get_session() as session:
            await session.execute(update(BetORM), list(map(asdict, bets)))

    async def change_bets_states(self, event_id: UUID, event_state: BetState) -> None:
        stmt = select(BetORM).where(BetORM.event_id == event_id)
        async with self.database.get_read_only_session() as session:
            orm_bets = await session.execute(stmt)
            bets = [orm_bet.to_entity() for orm_bet, *_ in orm_bets]

        for bet in bets: bet.state = event_state  # noqa
        await self.batch_bets_update(bets)

    async def get_bet(self, bet_id: UUID) -> Bet:
        bet = await self.get_by_bet_id(bet_id=bet_id)

        if not bet:
            raise BetNotFoundException()

        return bet

    async def get_bet_list(self) -> list[Bet]:
        stmt = select(BetORM)
        async with self.database.get_read_only_session() as session:
            orm_bets = await session.execute(stmt)
            return [orm_bet.to_entity() for orm_bet, *_ in orm_bets]

    async def get_or_create(self, bet: Bet) -> Bet:
        orm_bet = await self.get_by_bet_id(bet_id=bet.bet_id)
        if not orm_bet:
            orm_bet = await self.create(bet)

        return orm_bet

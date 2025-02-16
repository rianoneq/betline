import datetime
import uuid
from decimal import Decimal

import pytest
import pytz

from domain.commands.bet import (
    CreateBetCommand,
    GetBetCommand,
)
from domain.commands.event import (
    EventCreatedCommand,
    EventEndedCommand,
)
from domain.entities.bet import (
    Bet,
    BetState,
)
from domain.entities.event import (
    Event,
    EventState,
)
from domain.exceptions.bet import (
    BetAlreadyExistsException,
    BetNotFoundException,
)
from domain.exceptions.event import (
    CannotCompleteNotFoundEventException,
    EventAlreadyExistsException,
)
from services.bet.base import BaseBetService
from services.event.base import BaseEventService
from use_cases.bet import (
    CreateBetUseCase,
    GetBetUseCase,
)
from use_cases.event import (
    EventCreatedUseCase,
    EventEndedUseCase,
)


@pytest.fixture
async def create_use_case(container) -> CreateBetUseCase:
    return container.resolve(CreateBetUseCase)


@pytest.fixture
async def get_use_case(container) -> GetBetUseCase:
    return container.resolve(GetBetUseCase)


@pytest.fixture
async def event_ended_use_case(container) -> EventEndedUseCase:
    return container.resolve(EventEndedUseCase)


@pytest.fixture
async def event_created_use_case(container) -> EventCreatedUseCase:
    return container.resolve(EventCreatedUseCase)


@pytest.fixture
async def bet_service(container) -> BaseBetService:
    return container.resolve(BaseBetService)


@pytest.fixture
async def event_service(container) -> BaseEventService:
    return container.resolve(BaseEventService)


@pytest.fixture
async def event(event_service: BaseEventService) -> Event:
    return await event_service.get_or_create(
        Event(
            event_id=uuid.uuid4(),
            event_deadline=datetime.datetime.now() + datetime.timedelta(hours=1),
            completed=False,
        )
    )


@pytest.fixture
async def bet(event: Event, bet_service: BaseBetService) -> Bet:
    return await bet_service.get_or_create(
        Bet(
            bet_id=uuid.uuid4(),
            event_id=event.event_id,
            amount=Decimal(120),
            state=BetState.NEW,
        )
    )


async def mock_send_message(*args, **kwargs) -> None:
    return


async def test_create_bet(
    create_use_case: CreateBetUseCase,
    get_use_case: GetBetUseCase,
    event_ended_use_case: EventEndedUseCase,
    event_created_use_case: EventCreatedUseCase,
    bet_service: BaseBetService,
    event_service: BaseEventService,
    event: Event,
    bet: Bet,
    monkeypatch,
):
    monkeypatch.setattr(
        create_use_case.message_broker, "send_message", mock_send_message
    )
    with pytest.raises(BetAlreadyExistsException):
        await create_use_case.execute(CreateBetCommand(bet=bet))

    bet_id = uuid.uuid4()
    added_bet = await create_use_case.execute(
        CreateBetCommand(
            Bet(
                event_id=event.event_id,
                bet_id=bet_id,
                amount=Decimal(112),
                state=BetState.NEW,
            )
        )
    )

    gotten_bet = await bet_service.get_by_bet_id(bet_id=bet_id)
    assert gotten_bet.bet_id == added_bet.bet_id == bet_id

    # TODO разбить на разные тест кейсы
    await _get_bet(get_use_case, bet)
    await _event_ended_use_case(event_ended_use_case, bet, bet_service, event)
    await _event_created_use_case(event_created_use_case, event_service, event)


async def _get_bet(get_use_case: GetBetUseCase, bet: Bet):
    with pytest.raises(BetNotFoundException):
        await get_use_case.execute(GetBetCommand(bet_id=uuid.uuid4()))

    db_bet = await get_use_case.execute(
        GetBetCommand(bet_id=bet.bet_id)
    )

    assert db_bet.bet_id == bet.bet_id


async def _event_ended_use_case(
    event_ended_use_case: EventEndedUseCase,
    bet: Bet,
    bet_service: BaseBetService,
    event: Event,
):

    with pytest.raises(CannotCompleteNotFoundEventException):
        await event_ended_use_case.execute(
            EventEndedCommand(
                event_id=uuid.uuid4(),
                event_state=EventState.FINISHED_WIN,
            )
        )

    await event_ended_use_case.execute(
        EventEndedCommand(
            event_id=event.event_id,
            event_state=EventState.FINISHED_WIN,
        )
    )

    db_bet = await bet_service.get_by_bet_id(bet_id=bet.bet_id)
    assert db_bet.state == EventState.FINISHED_WIN


async def _event_created_use_case(
        event_created_use_case: EventCreatedUseCase,
        event_service: BaseEventService,
        event: Event,
):

    with pytest.raises(EventAlreadyExistsException):
        await event_created_use_case.execute(
            EventCreatedCommand(
                event_id=event.event_id,
                event_deadline=datetime.datetime.now() + datetime.timedelta(hours=1),
            )
        )
    event_id = uuid.uuid4()
    new_event = await event_created_use_case.execute(
        EventCreatedCommand(
            event_id=event_id,
            event_deadline=datetime.datetime.now(tz=pytz.UTC) + datetime.timedelta(hours=1),
        )
    )

    db_event = await event_service.get_event(event_id)

    assert db_event
    assert new_event.event_id == db_event.event_id
    assert new_event.event_deadline == db_event.event_deadline
    assert not db_event.completed

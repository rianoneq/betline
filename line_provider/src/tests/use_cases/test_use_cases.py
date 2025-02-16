import dataclasses
import datetime
import uuid
from decimal import Decimal

import pytest
import pytz

from domain.commands.bet import NewBetCommand
from domain.commands.event import (
    GetEventCommand,
    UpdateEventCommand,
)
from domain.entities.event import (
    Event,
    EventState,
)
from domain.exceptions import (
    EventAlreadyExistsException,
    EventNotFoundException,
    EventStateAlreadyChangedException,
)
from services.base import BaseEventService
from use_cases.bet.bet import BetCreatedUseCase
from use_cases.event.event import (
    CreateEventCommand,
    CreateEventUseCase,
    GetEventUseCase,
    UpdateEventUseCase,
)


@pytest.fixture
async def create_use_case(container) -> CreateEventUseCase:
    return container.resolve(CreateEventUseCase)


@pytest.fixture
async def get_use_case(container) -> GetEventUseCase:
    return container.resolve(GetEventUseCase)


@pytest.fixture
async def update_use_case(container) -> UpdateEventUseCase:
    return container.resolve(UpdateEventUseCase)


@pytest.fixture
async def new_bet_use_case(container) -> BetCreatedUseCase:
    return container.resolve(BetCreatedUseCase)


@pytest.fixture
async def event_service(container) -> BaseEventService:
    return container.resolve(BaseEventService)


@pytest.fixture
async def event(event_service: BaseEventService) -> Event:
    return await event_service.get_or_create(
        Event(
            event_id=uuid.uuid4(),
            coefficient=Decimal(10),
            deadline=datetime.datetime.now(tz=pytz.UTC) + datetime.timedelta(hours=1),
            state=EventState.NEW,
        )
    )


async def mock_send_message(*args, **kwargs) -> None:
    return


async def test_create_event(
    create_use_case: CreateEventUseCase,
    update_use_case: UpdateEventUseCase,
    get_use_case: GetEventUseCase,
    new_bet_use_case: BetCreatedUseCase,
    event_service: BaseEventService,
    event: Event,
    monkeypatch,
):
    monkeypatch.setattr(
        create_use_case.message_broker, "send_message", mock_send_message
    )

    with pytest.raises(EventAlreadyExistsException):
        await create_use_case.execute(CreateEventCommand(event=event))

    event_id = uuid.uuid4()

    added_event = await create_use_case.execute(
        CreateEventCommand(
            Event(
                coefficient=Decimal(10),
                event_id=event_id,
                deadline=datetime.datetime.now(tz=pytz.UTC) + datetime.timedelta(hours=1),
                state=EventState.NEW,
            )
        )
    )

    gotten_event = await event_service.get_by_event_id(event_id=event_id)
    assert gotten_event.event_id == added_event.event_id == event_id

    # TODO разбить на разные тест кейсы
    await _update_event(update_use_case, event_service, event)
    await _get_event(get_use_case, event)
    await _new_bet(new_bet_use_case, event_service, event)


async def _update_event(
    update_use_case: UpdateEventUseCase,
    event_service: BaseEventService,
    event: Event,
):
    with pytest.raises(EventNotFoundException):
        fake_event = dataclasses.replace(event)
        fake_event.event_id = uuid.uuid4()

        await update_use_case.execute(
            UpdateEventCommand(
                event_id=fake_event.event_id, state=fake_event.state
            )
        )

    await update_use_case.execute(
        UpdateEventCommand(event_id=event.event_id, state=EventState.FINISHED_WIN)
    )

    db_event = await event_service.get_by_event_id(event_id=event.event_id)

    assert db_event.state == EventState.FINISHED_WIN
    # float(db_event.coefficient) == 9 and
    with pytest.raises(EventStateAlreadyChangedException):
        await update_use_case.execute(
            UpdateEventCommand(
                event_id=event.event_id, state=EventState.FINISHED_WIN
            )
        )


async def _get_event(get_use_case: GetEventUseCase, event: Event):
    with pytest.raises(EventNotFoundException):
        await get_use_case.execute(GetEventCommand(event_id=uuid.uuid4()))

    db_event = await get_use_case.execute(
        GetEventCommand(event_id=event.event_id)
    )

    assert db_event.event_id == event.event_id


async def _new_bet(
        new_bet_use_case: BetCreatedUseCase,
        event_service: BaseEventService,
        event: Event,
):  
    with pytest.raises(EventNotFoundException):
        await new_bet_use_case.execute(NewBetCommand(event_id=uuid.uuid4(), bet_amount=50))

    db_event = await new_bet_use_case.execute(
        NewBetCommand(event_id=event.event_id, bet_amount=50)
    )

    db_event = await event_service.get_event(event.event_id)

    assert db_event.event_id == event.event_id and db_event.coefficient == 5

    db_event = await new_bet_use_case.execute(
        NewBetCommand(event_id=event.event_id, bet_amount=50)
    )

    db_event = await event_service.get_event(event.event_id)

    assert db_event.coefficient == 1

    db_event = await new_bet_use_case.execute(
        NewBetCommand(event_id=event.event_id, bet_amount=50)
    )
    db_event = await event_service.get_event(event.event_id)
    assert db_event.coefficient == 1

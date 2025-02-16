from contextlib import asynccontextmanager

from fastapi import FastAPI

from aiojobs import Scheduler

from core.configs import settings
from core.container import get_container
from infra.converters.event import (
    convert_event_changed_message_to_command,
    convert_new_event_message_to_command,
)
from infra.message_broker.base import BaseMessageBroker
from use_cases.event import (
    EventCreatedUseCase,
    EventEndedUseCase,
)


async def event_change_consumer():
    container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    use_case: EventEndedUseCase = container.resolve(EventEndedUseCase)

    async for message in message_broker.start_consuming(settings.event_change_topic):
        await use_case.execute(convert_event_changed_message_to_command(message))


async def new_event_consumer():
    container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    use_case: EventCreatedUseCase = container.resolve(EventCreatedUseCase)

    async for message in message_broker.start_second_consuming(
        settings.new_event_topic
    ):
        await use_case.execute(convert_new_event_message_to_command(message))


async def init_message_broker():
    container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start()


async def close_message_broker():
    container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()

    container = get_container()
    scheduler: Scheduler = container.resolve(Scheduler)

    event_change_consumer_job = await scheduler.spawn(event_change_consumer())
    new_event_consumer_job = await scheduler.spawn(new_event_consumer())

    yield

    await close_message_broker()
    await event_change_consumer_job.close()
    await new_event_consumer_job.close()

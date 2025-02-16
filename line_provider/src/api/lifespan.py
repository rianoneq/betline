from contextlib import asynccontextmanager

from fastapi import FastAPI

from aiojobs import Scheduler

from core.configs import settings
from core.containers import get_container
from infra.converters.bet import convert_new_bet_message_to_command
from infra.message_broker.base import BaseMessageBroker
from use_cases.bet.bet import BetCreatedUseCase


async def new_bet_consumer():
    container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    use_case: BetCreatedUseCase = container.resolve(BetCreatedUseCase)

    async for message in message_broker.start_consuming(
        settings.new_bet_topic,
    ):
        await use_case.execute(convert_new_bet_message_to_command(message))


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
    new_bet_consumer_job = await scheduler.spawn(new_bet_consumer())

    yield

    await new_bet_consumer_job.close()
    await close_message_broker()

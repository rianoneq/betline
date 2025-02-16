from functools import lru_cache
from uuid import uuid4

from aiojobs import Scheduler
from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)
from gateways.postgresql.database import Database
from punq import (
    Container,
    Scope,
)

from core.configs import settings
from domain.commands.event import (
    CreateEventCommand,
    GetEventCommand,
    GetEventListCommand,
    UpdateEventCommand,
)
from infra.message_broker.base import BaseMessageBroker
from infra.message_broker.kafka import KafkaMessageBroker
from services.base import BaseEventService
from services.event import ORMEventService
from use_cases.bet.bet import BetCreatedUseCase
from use_cases.event.event import (
    CreateEventUseCase,
    GetEventListUseCase,
    GetEventUseCase,
    UpdateEventUseCase,
)


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(
        Database,
        scope=Scope.singleton,
        factory=lambda: Database(
            url=settings.POSTGRES_DB_URL,
            ro_url=settings.POSTGRES_DB_URL,
        ),
    )

    # services
    container.register(BaseEventService, ORMEventService)

    # commands
    container.register(CreateEventCommand)
    container.register(GetEventListCommand)
    container.register(GetEventCommand)
    container.register(UpdateEventCommand)

    def create_message_broker() -> BaseMessageBroker:  # noqa: F821
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=settings.kafka_url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=settings.kafka_url,
                group_id=f"events-{uuid4()}",
                metadata_max_age_ms=30000,
            ),
        )

    # message broker
    container.register(
        BaseMessageBroker, factory=create_message_broker, scope=Scope.singleton,
    )

    # use cases
    container.register(CreateEventUseCase)
    container.register(GetEventUseCase)
    container.register(GetEventListUseCase)
    container.register(UpdateEventUseCase)
    container.register(BetCreatedUseCase)

    container.register(Scheduler, factory=lambda: Scheduler(), scope=Scope.singleton)

    return container

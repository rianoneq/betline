from functools import lru_cache
from uuid import uuid4

from aiojobs import Scheduler
from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)
from punq import (
    Container,
    Scope,
)

from core.configs import settings
from domain.commands.bet import (
    CreateBetCommand,
    GetBetCommand,
    GetBetListCommand,
)
from gateways.postgresql.database import Database
from infra.message_broker.base import BaseMessageBroker
from infra.message_broker.kafka import KafkaMessageBroker
from services.bet.base import BaseBetService
from services.bet.bet import ORMBetService
from services.event.base import BaseEventService
from services.event.event import ORMEventService
from use_cases.bet import (
    CreateBetUseCase,
    GetBetListUseCase,
    GetBetUseCase,
)
from use_cases.event import (
    EventCreatedUseCase,
    EventEndedUseCase,
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

    def create_message_broker() -> BaseMessageBroker:  # noqa: F821
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=settings.kafka_url),
            new_event_consumer=AIOKafkaConsumer(
                bootstrap_servers=settings.kafka_url,
                group_id=f"events-{uuid4()}",
                metadata_max_age_ms=30000,
            ),
            changed_event_consumer=AIOKafkaConsumer(
                bootstrap_servers=settings.kafka_url,
                group_id=f"events-{uuid4()}",
                metadata_max_age_ms=30000,
            ),
        )

    # message broker
    container.register(
        BaseMessageBroker,
        factory=create_message_broker,
        scope=Scope.singleton,
    )

    # services
    container.register(BaseBetService, ORMBetService)
    container.register(BaseEventService, ORMEventService)

    # use cases
    container.register(CreateBetUseCase)
    container.register(GetBetListUseCase)
    container.register(GetBetUseCase)
    container.register(EventEndedUseCase)
    container.register(EventCreatedUseCase)

    # commands
    container.register(CreateBetCommand)
    container.register(GetBetCommand)
    container.register(GetBetListCommand)

    container.register(Scheduler, factory=lambda: Scheduler(), scope=Scope.singleton)

    return container

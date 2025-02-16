from dataclasses import dataclass
from typing import AsyncIterator

import orjson
from aiokafka import AIOKafkaConsumer
from aiokafka.producer import AIOKafkaProducer

from infra.message_broker.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    new_event_consumer: AIOKafkaConsumer
    changed_event_consumer: AIOKafkaConsumer

    async def send_message(self, key: bytes, topic: str, value: bytes):
        await self.producer.send(topic=topic, key=key, value=value)

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        self.changed_event_consumer.subscribe(topics=[topic])

        async for message in self.changed_event_consumer:
            yield orjson.loads(message.value)

    async def start_second_consuming(self, topic: str) -> AsyncIterator[dict]:
        self.new_event_consumer.subscribe(topics=[topic])

        async for message in self.new_event_consumer:
            yield orjson.loads(message.value)

    async def stop_consuming(self):
        self.new_event_consumer.unsubscribe()
        self.changed_event_consumer.unsubscribe()

    async def close(self):
        await self.new_event_consumer.stop()
        await self.changed_event_consumer.stop()
        await self.producer.stop()

    async def start(self):
        await self.producer.start()
        await self.new_event_consumer.start()
        await self.changed_event_consumer.start()

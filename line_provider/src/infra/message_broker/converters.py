from dataclasses import asdict

import orjson

from domain.messages.base import BaseMessage


def convert_message_to_broker_message(message: BaseMessage) -> bytes:
    return orjson.dumps(message)


def convert_message_to_json(message: BaseMessage) -> dict[str, any]:
    return asdict(message)

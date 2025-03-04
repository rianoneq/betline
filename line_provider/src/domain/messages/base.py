from abc import ABC
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import ClassVar
from uuid import (
    UUID,
    uuid4,
)


@dataclass
class BaseMessage(ABC):
    message_title: ClassVar[str]

    message_id: UUID = field(default_factory=uuid4, kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)

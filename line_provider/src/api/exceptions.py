from dataclasses import (
    dataclass,
    field,
)
from functools import partial
from typing import (
    Awaitable,
    Callable,
)

from fastapi import (
    FastAPI,
    Request,
    status,
)
from fastapi.responses import JSONResponse

from domain.exceptions import (
    BaseDomainException,
    EventAlreadyExistsException,
    EventNotFoundException,
    EventStateAlreadyChangedException,
)


@dataclass(frozen=True)
class ErrorResponse:
    status_code: int
    data: dict = field(default_factory=dict)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BaseDomainException, error_handler(500))
    app.add_exception_handler(
        EventNotFoundException, error_handler(status.HTTP_404_NOT_FOUND)
    )
    app.add_exception_handler(
        EventAlreadyExistsException, error_handler(status.HTTP_409_CONFLICT)
    )
    app.add_exception_handler(
        EventStateAlreadyChangedException, error_handler(status.HTTP_409_CONFLICT)
    )


def error_handler(status_code: int) -> Callable[..., Awaitable]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(
    request: Request, err: BaseDomainException, status_code: int
):
    return JSONResponse(status_code=status_code,
                        content={'message': err.message})

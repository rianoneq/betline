from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from punq import Container

from api.v1.schemas import (
    ApiResponse,
    CreateEventInSchema,
    ErrorSchema,
    EventOutSchema,
    ListPaginatedResponse,
    PaginationOutSchema,
    UpdateEventInSchema,
)
from core.containers import get_container
from domain.commands.event import (
    CreateEventCommand,
    GetEventCommand,
    UpdateEventCommand,
)
from use_cases.event.event import (
    CreateEventUseCase,
    GetEventListUseCase,
    GetEventUseCase,
    UpdateEventUseCase,
)


router = APIRouter()


@router.get(
    "/",
    response_model=ApiResponse[ListPaginatedResponse[EventOutSchema]],
    status_code=status.HTTP_200_OK,
    description="Ручка на получение всех эвентов",
    responses={
        status.HTTP_200_OK: {"model": ListPaginatedResponse[EventOutSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_all_events(
    container: Container = Depends(get_container),
) -> ApiResponse[ListPaginatedResponse[EventOutSchema]]:
    use_case: GetEventListUseCase = container.resolve(GetEventListUseCase)
    events = await use_case.execute()

    response = ListPaginatedResponse(
        items=[EventOutSchema.from_entity(event) for event in events],
        pagination=PaginationOutSchema(
        ),
    )
    return ApiResponse(data=response)


@router.get(
    "/{event_id}",
    response_model=ApiResponse[EventOutSchema],
    status_code=status.HTTP_200_OK,
    description="Ручка на получение определенного эвента",
    responses={
        status.HTTP_200_OK: {"model": EventOutSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def get_event_view(
    event_id: UUID,
    container: Container = Depends(get_container),
) -> ApiResponse[EventOutSchema]:
    use_case: GetEventUseCase = container.resolve(GetEventUseCase)
    command = GetEventCommand(event_id=event_id)

    event = await use_case.execute(command)

    return ApiResponse(data=EventOutSchema.from_entity(event))


@router.post(
    "/{event_id}",
    response_model=ApiResponse[EventOutSchema],
    status_code=status.HTTP_201_CREATED,
    description="Ручка на добавление нового эвента",
    responses={
        status.HTTP_201_CREATED: {"model": EventOutSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorSchema},
    },
)
async def create_event_view(
    event_in: CreateEventInSchema,
    event_id: UUID,
    container: Container = Depends(get_container),
) -> ApiResponse[EventOutSchema]:
    use_case: CreateEventUseCase = container.resolve(CreateEventUseCase)
    command = CreateEventCommand(event=event_in.to_entity(event_id))

    event = await use_case.execute(command)

    return ApiResponse(data=EventOutSchema.from_entity(event))


@router.put(
    "/{event_id}",
    response_model=ApiResponse[EventOutSchema],
    status_code=status.HTTP_200_OK,
    description="Ручка на изменение эвента",
    responses={
        status.HTTP_200_OK: {"model": EventOutSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def update_event_view(
    event_in: UpdateEventInSchema,
    event_id: UUID,
    container: Container = Depends(get_container),
) -> ApiResponse[EventOutSchema]:
    use_case: UpdateEventUseCase = container.resolve(UpdateEventUseCase)
    command = UpdateEventCommand(event_id=event_id,
                                 state=event_in.state)
    event = await use_case.execute(command)

    return ApiResponse(data=EventOutSchema.from_entity(event))

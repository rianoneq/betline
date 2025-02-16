from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from punq import Container

from api.v1.schemas import (
    ApiResponse,
    BetOutSchema,
    CreateBetInSchema,
    ErrorSchema,
)
from core.container import get_container
from domain.commands.bet import (
    CreateBetCommand,
    GetBetCommand,
)
from use_cases.bet import (
    CreateBetUseCase,
    GetBetListUseCase,
    GetBetUseCase,
)


router = APIRouter()


@router.get(
    "/",
    response_model=ApiResponse[list[BetOutSchema]],
    status_code=status.HTTP_200_OK,
    description="Ручка на получение всех ставок",
    responses={
        status.HTTP_200_OK: {"model": list[BetOutSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_all_bets(
    container: Container = Depends(get_container),
) -> ApiResponse[list[BetOutSchema]]:
    use_case: GetBetListUseCase = container.resolve(GetBetListUseCase)
    bets = await use_case.execute()

    response = [BetOutSchema.from_entity(bet) for bet in bets]
    return ApiResponse(data=response)


@router.get(
    "/{bet_id}",
    response_model=ApiResponse[BetOutSchema],
    status_code=status.HTTP_200_OK,
    description="Ручка на получение определенной ставки",
    responses={
        status.HTTP_200_OK: {"model": BetOutSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def get_bet_view(
    bet_id: UUID,
    container: Container = Depends(get_container),
) -> ApiResponse[BetOutSchema]:
    use_case: GetBetUseCase = container.resolve(GetBetUseCase)
    command = GetBetCommand(bet_id=bet_id)

    bet = await use_case.execute(command)

    return ApiResponse(data=BetOutSchema.from_entity(bet))


@router.post(
    "/{bet_id}",
    response_model=ApiResponse[BetOutSchema],
    status_code=status.HTTP_201_CREATED,
    description="Ручка на добавление новой ставки",
    responses={
        status.HTTP_201_CREATED: {"model": BetOutSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorSchema},
    },
)
async def create_bet_view(
    bet_in: CreateBetInSchema,
    bet_id: UUID,
    container: Container = Depends(get_container),
) -> ApiResponse[BetOutSchema]:
    use_case: CreateBetUseCase = container.resolve(CreateBetUseCase)
    command = CreateBetCommand(bet=bet_in.to_entity(bet_id=bet_id))

    bet = await use_case.execute(command)

    return ApiResponse(data=BetOutSchema.from_entity(bet))

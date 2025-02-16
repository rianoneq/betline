from fastapi import APIRouter

from api.v1.views import bets


api_router = APIRouter()
api_router.include_router(bets.router, prefix='/bets', tags=['bets'])

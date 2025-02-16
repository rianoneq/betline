from fastapi import APIRouter

from api.v1.views import events


api_router = APIRouter()
api_router.include_router(events.router, prefix='/events', tags=['events'])

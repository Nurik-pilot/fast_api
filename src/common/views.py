from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import (
    get_db, get_settings, get_cache,
)
from core.settings import Settings
from .clients import RedisClient
from .repositories import StateRepository
from .schemas import StateResponse

common_router = APIRouter()


@common_router.get(
    path='/state/', status_code=200,
    response_model=StateResponse,
)
def state(
    settings: Settings = Depends(
        dependency=get_settings,
    ),
    db: type[Session] = Depends(
        dependency=get_db,
    ),
    cache: RedisClient = Depends(
        dependency=get_cache,
    ),
) -> StateResponse:
    repository = StateRepository(
        cache=cache, db=db,
        rabbitmq_url=settings.celery_broker_url,
    )
    return StateResponse(
        database_works=repository.database_works,
        cache_works=repository.cache_works,
        broker_works=repository.broker_works,
    )

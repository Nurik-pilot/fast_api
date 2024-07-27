from fastapi import FastAPI
from fastapi.responses import (
    ORJSONResponse,
)
from sentry_sdk import init
from starlette.middleware.cors import (
    CORSMiddleware,
)

from common.views import common_router
from faas.views import faas_router
from .settings import Settings

settings: Settings = Settings()

init(dsn=settings.sentry_dsn)

main_app: FastAPI = FastAPI(
    debug=settings.debug,
    default_response_class=ORJSONResponse,
    version=settings.version,
    title=settings.title,
)
main_app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=('*',),
    allow_credentials=True,
    allow_methods=('*',),
    allow_headers=('*',),
)

main_app.include_router(
    router=common_router, prefix='/api',
)
main_app.include_router(
    router=faas_router, prefix='/api',
)

app = main_app

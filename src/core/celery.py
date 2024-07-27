from celery import Celery
from sentry_sdk import init
from sentry_sdk.integrations.celery import (
    CeleryIntegration,
)

from .dependencies import get_settings
from .settings import Settings

settings: Settings = get_settings()
sentry_dsn = settings.sentry_dsn
init(
    dsn=sentry_dsn,
    integrations=(CeleryIntegration(),),
)

broker = settings.celery_broker_url
backend = settings.celery_result_backend
celery_app: Celery = Celery(
    main='core', broker=broker,
    backend=backend,
)

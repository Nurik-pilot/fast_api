from pydantic import (
    AmqpDsn, Extra, Field,
)
from pydantic_settings import (
    BaseSettings, SettingsConfigDict,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='/src/core/.env',
        extra=Extra.allow,
    )
    debug: bool = Field(alias='DEBUG')
    version: str = Field(
        alias='VERSION', default='0.1.0',
    )
    title: str = Field(
        alias='TITLE', default='seed',
    )

    postgres_url: str = Field(
        alias='POSTGRES_URL',
    )

    celery_broker_url: AmqpDsn = Field(
        alias='CELERY_BROKER_URL',
    )
    celery_result_backend: str = Field(
        alias='CELERY_RESULT_BACKEND',
    )

    s3_access_key_id: str = Field(
        alias='S3_ACCESS_KEY_ID',
    )
    s3_secret_access_key: str = Field(
        alias='S3_SECRET_ACCESS_KEY',
    )
    s3_endpoint_url: str | None = Field(
        alias='S3_ENDPOINT_URL', default=None,
    )
    s3_bucket_name: str = Field(
        alias='S3_BUCKET_NAME',
    )

    redis_url: str = Field(alias='REDIS_URL')

    sentry_dsn: str = Field(
        alias='SENTRY_DSN', default='',
    )

    secret_key: str = Field(alias='SECRET_KEY')

    algorithm: str = Field(
        alias='ALGORITHM', default='HS256',
    )

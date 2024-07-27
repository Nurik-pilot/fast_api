from uuid import uuid4

from kombu import Connection
from pydantic import AmqpDsn
from sqlalchemy import (
    text, Row, Result,
)
from sqlalchemy.orm import Session

from common.clients import (
    RedisClient, ExchangeType,
    ExchangeConfiguration,
    RabbitMQClient,
)


class StateRepository:
    db: type[Session]
    redis_url: str
    rabbitmq_url: AmqpDsn

    def __init__(
        self, db: type[Session],
        cache: RedisClient,
        rabbitmq_url: AmqpDsn,
    ) -> None:
        super().__init__()
        self.db = db
        self.cache = cache
        self.rabbitmq_url = rabbitmq_url

    @property
    def database_works(self) -> bool:
        response: Row | None
        cursor: Result
        with self.db(
        ) as session, session.begin():
            cursor = session.execute(
                statement=text(
                    text='select 1;',
                ),
            )
            response = cursor.fetchone()
        return response == (1,)

    @property
    def cache_works(self) -> bool:
        key, value = 'foo', 'bar'
        self.cache.put(
            key=key, value=value,
        )
        return self.cache.get(
            key=key,
        ) == value

    @property
    def broker_works(self) -> bool:
        routing_key = str(uuid4())
        configuration = ExchangeConfiguration(
            exchange_name=str(uuid4()),
            exchange_type=ExchangeType.direct,
            durable=True,
        )
        _ = RabbitMQClient(
            rabbit_mq_url=self.rabbitmq_url,
            exchange_configuration=configuration,
            routing_key=routing_key,
        )
        with Connection(
            hostname=str(_.rabbit_mq_url),
            transport_options=_.transport_options,
        ) as connection:
            return isinstance(
                connection.ensure_connection(),
                Connection,
            )

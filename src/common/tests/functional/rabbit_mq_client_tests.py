from typing import Any
from uuid import uuid4

from kombu import Message

from common.clients import (
    ExchangeType,
    ExchangeConfiguration,
    RabbitMQClient,
)
from core.settings import Settings


def test_rabbitmq_client(
    test_settings: Settings,
) -> None:
    routing_key = str(uuid4())
    queue_name = str(uuid4())
    message_body = {'hello': 'world'}
    configuration: ExchangeConfiguration
    configuration = ExchangeConfiguration(
        exchange_name=str(uuid4()),
        exchange_type=ExchangeType.direct,
        durable=True,
    )
    _ = test_settings
    rabbit_mq_client = RabbitMQClient(
        rabbit_mq_url=_.celery_broker_url,
        exchange_configuration=configuration,
        routing_key=routing_key,
    )

    def call_back(
        body: dict[str, Any],
        message: Message,
    ) -> None:
        assert message_body == body
        message.ack()

    rabbit_mq_client.consume(
        queue_name=queue_name,
        call_back=call_back,
    )
    rabbit_mq_client.publish(
        message_body=message_body,
    )
    rabbit_mq_client.consume(
        queue_name=queue_name,
        call_back=call_back,
    )
    rabbit_mq_client.publish(
        message_body=message_body,
    )
    rabbit_mq_client.consume(
        queue_name=queue_name,
        call_back=call_back,
    )

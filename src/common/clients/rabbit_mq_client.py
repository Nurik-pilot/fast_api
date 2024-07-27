from enum import Enum
from typing import Callable, Any

from kombu import (
    Producer, Connection,
    Exchange, Queue,
)
from pydantic import BaseModel, AmqpDsn


class ExchangeType(str, Enum):
    direct: str = 'direct'
    fanout: str = 'fanout'
    topic: str = 'topic'


class ExchangeConfiguration(BaseModel):
    exchange_name: str
    durable: bool
    exchange_type: ExchangeType


class RabbitMQClient:
    def __init__(
        self,
        rabbit_mq_url: AmqpDsn,
        routing_key: str,
        exchange_configuration: ExchangeConfiguration,
    ) -> None:
        """
        Generic rabbit mq client

        :param rabbit_mq_url:
        :param routing_key:
        :param exchange_configuration:
        """
        super().__init__()
        self.rabbit_mq_url = rabbit_mq_url
        self.routing_key = routing_key
        self.exchange = Exchange(
            name=exchange_configuration.exchange_name,
            type=exchange_configuration.exchange_type,
            durable=exchange_configuration.durable,
        )
        self.transport_options = {'confirm_publish': True}

    def publish(
        self, message_body: dict[str, Any],
    ) -> None:
        with Connection(
            hostname=str(self.rabbit_mq_url),
            transport_options=self.transport_options,
        ) as connection, connection.channel() as channel:
            producer = Producer(
                channel=channel,
                exchange=self.exchange,
                auto_declare=True,
                routing_key=self.routing_key,

            )
            producer.publish(
                body=message_body,
                retry=True,
                retry_policy={
                    'interval_start': 0,
                    'interval_step': 1,
                    'interval_max': 16,
                    'max_retries': 16,
                },
            )

    def consume(
        self,
        queue_name: str,
        call_back: Callable,
    ) -> None:
        queue = Queue(
            name=queue_name,
            exchange=self.exchange,
            routing_key=self.routing_key,
        )
        with Connection(
            hostname=str(self.rabbit_mq_url),
            transport_options=self.transport_options,
        ) as connection, connection.Consumer(
            queues=(queue,),
        ) as consumer:
            consumer.register_callback(callback=call_back)
            consumer.consume()

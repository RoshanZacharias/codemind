import json

import aio_pika

from ..config import settings


async def publish_message(queue_name: str, message: dict) -> None:
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(
            queue_name,
            durable=True,
        )

        message_body = json.dumps(message).encode()

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body,
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=queue.name,
        )
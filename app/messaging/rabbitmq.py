import pika
import json
from app.config import settings

def get_channel():
    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue="order_created", durable=True)
    return connection, channel

def publish_order_created(order_data: dict, channel=None):
    if channel is None:
        connection, channel = get_channel()
        close_connection = True
    else:
        close_connection = False

    queue_name = "order_created"
    channel.basic_publish(
        exchange="",
        routing_key="order_created",
        body=json.dumps(order_data),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    if close_connection:
        connection.close()


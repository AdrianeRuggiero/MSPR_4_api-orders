import pika
import json
from app.config import settings

def publish_order_created(order_data: dict):
    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel = connection.channel()

    queue_name = "order_created"
    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(order_data),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()

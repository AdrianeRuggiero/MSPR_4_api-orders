from unittest.mock import MagicMock, patch
from app.messaging import rabbitmq


def test_get_channel_opens_connection():
    with patch("app.messaging.rabbitmq.pika.BlockingConnection") as mock_conn:
        mock_channel = MagicMock()
        mock_conn.return_value.channel.return_value = mock_channel

        conn, chan = rabbitmq.get_channel()

        mock_conn.assert_called_once()
        mock_channel.queue_declare.assert_called_once_with(queue="order_created", durable=True)
        assert chan == mock_channel
        assert conn is mock_conn.return_value


@patch("app.messaging.rabbitmq.get_channel")
def test_publish_order_created_with_auto_connection(mock_get_channel):
    mock_conn = MagicMock()
    mock_chan = MagicMock()
    mock_get_channel.return_value = (mock_conn, mock_chan)

    order_data = {"client_id": "test", "products": [], "total_price": 0}
    rabbitmq.publish_order_created(order_data)

    mock_chan.basic_publish.assert_called_once()
    mock_conn.close.assert_called_once()

def test_publish_order_created_real(monkeypatch):
    class DummyChannel:
        def queue_declare(self, queue, durable): pass
        def basic_publish(self, exchange, routing_key, body, properties): pass
        def close(self): pass

    class DummyConnection:
        def channel(self):
            return DummyChannel()
        def close(self): pass

    # Simule la connexion Pika
    monkeypatch.setattr("pika.BlockingConnection", lambda x: DummyConnection())

    from app.messaging.rabbitmq import publish_order_created

    order_data = {
        "client_id": "x",
        "products": [{"product_id": "p", "quantity": 1}],
        "total_price": 10.0
    }

    publish_order_created(order_data)

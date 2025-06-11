from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models.order import OrderCreate, OrderProduct
from app.services.order_service import OrderService
from app.security.auth import create_access_token
import app.messaging.rabbitmq as rabbitmq
import json

client = TestClient(app)

def get_auth_headers(role="admin"):
    token = create_access_token({"sub": "tester", "role": role})
    return {"Authorization": f"Bearer {token}"}

@patch("app.services.order_service.publish_order_created", lambda x: None)
def test_create_order():
    payload = {
        "client_id": "client1",
        "products": [{"product_id": "prod1", "quantity": 2}],
        "total_price": 50.0
    }
    response = client.post("/orders/", json=payload, headers=get_auth_headers())
    assert response.status_code == 201
    assert response.json()["client_id"] == "client1"

def test_list_orders():
    response = client.get("/orders/", headers=get_auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch("app.services.order_service.publish_order_created", lambda x: None)
def test_get_order_by_id():
    payload = {
        "client_id": "client2",
        "products": [{"product_id": "prod2", "quantity": 1}],
        "total_price": 20.0
    }
    create_resp = client.post("/orders/", json=payload, headers=get_auth_headers())
    order_id = create_resp.json()["id"]

    get_resp = client.get(f"/orders/{order_id}", headers=get_auth_headers())
    assert get_resp.status_code == 200
    assert get_resp.json()["client_id"] == "client2"

@patch("app.services.order_service.publish_order_created", lambda x: None)
def test_delete_order():
    payload = {
        "client_id": "client3",
        "products": [{"product_id": "prod3", "quantity": 3}],
        "total_price": 90.0
    }
    create_resp = client.post("/orders/", json=payload, headers=get_auth_headers())
    order_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/orders/{order_id}", headers=get_auth_headers())
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/orders/{order_id}", headers=get_auth_headers())
    assert get_resp.status_code == 404

def test_unauthorized_access():
    response = client.get("/orders/")
    assert response.status_code == 401

def test_forbidden_access():
    token = create_access_token({"sub": "user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/orders/", headers=headers)
    assert response.status_code == 403

def test_metrics_route():
    response = client.get("/metrics")
    assert response.status_code == 200

@patch("app.messaging.rabbitmq.get_channel")
def test_publish_order_created(mock_get_channel):
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_get_channel.return_value = (mock_connection, mock_channel)  # retourne bien 2 objets

    order_data = {
        "client_id": "x",
        "products": [{"product_id": "p", "quantity": 1}],
        "total_price": 10.0
    }

    rabbitmq.publish_order_created(order_data)

    mock_channel.basic_publish.assert_called_once()
    mock_connection.close.assert_called_once()
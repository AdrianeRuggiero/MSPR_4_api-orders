import pytest
from unittest.mock import MagicMock, patch
from app.models.order import OrderCreate, OrderProduct
from app.services.order_service import OrderService

@pytest.fixture
def mock_collection():
    return MagicMock()

@pytest.fixture
def service(mock_collection):
    return OrderService(mock_collection)

@patch("app.services.order_service.publish_order_created")
def test_create_order(mock_publish, service):
    order = OrderCreate(
        client_id="cli123",
        products=[OrderProduct(product_id="x", quantity=1)],
        total_price=10.0
    )
    result = service.create_order(order)
    assert result.client_id == "cli123"
    mock_publish.assert_called_once()

def test_get_order_found(service, mock_collection):
    mock_collection.find_one.return_value = {
        "id": "id1",
        "client_id": "cli123",
        "products": [{"product_id": "x", "quantity": 1}],
        "total_price": 10.0,
        "status": "pending",
        "created_at": "2024-01-01T00:00:00Z"
    }
    order = service.get_order("id1")
    assert order.id == "id1"

def test_get_order_not_found(service):
    service.collection.find_one.return_value = None
    order = service.get_order("unknown")
    assert order is None

def test_get_all_orders(service, mock_collection):
    mock_collection.find.return_value = [
        {
            "id": "id1",
            "client_id": "cliA",
            "products": [{"product_id": "x", "quantity": 1}],
            "total_price": 10.0,
            "status": "pending",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
    orders = service.get_all_orders()
    assert len(orders) == 1
    assert orders[0].client_id == "cliA"

def test_delete_order_success(service):
    service.collection.delete_one.return_value.deleted_count = 1
    result = service.delete_order("id123")
    assert result is True

def test_delete_order_fail(service):
    service.collection.delete_one.return_value.deleted_count = 0
    result = service.delete_order("unknown")
    assert result is False

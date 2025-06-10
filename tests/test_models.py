from app.models.order import OrderCreate, OrderProduct, OrderDB
from datetime import datetime

def test_order_product_model():
    product = OrderProduct(product_id="abc123", quantity=2)
    assert product.product_id == "abc123"
    assert product.quantity == 2

def test_order_create_model():
    order = OrderCreate(
        client_id="client1",
        products=[OrderProduct(product_id="p1", quantity=1)],
        total_price=15.0
    )
    assert order.client_id == "client1"
    assert order.total_price == 15.0
    assert order.status == "pending"
    assert isinstance(order.created_at, datetime)

def test_order_db_model():
    order = OrderDB(
        client_id="client2",
        products=[OrderProduct(product_id="p2", quantity=3)],
        total_price=45.0
    )
    assert order.id is not None
    assert isinstance(order.id, str)

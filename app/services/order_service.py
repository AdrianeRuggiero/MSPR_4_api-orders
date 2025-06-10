from typing import List, Optional
from pymongo.collection import Collection
from app.models.order import OrderCreate, OrderDB
from bson import ObjectId
from app.messaging.rabbitmq import publish_order_created


class OrderService:
    def __init__(self, orders_collection: Collection):
        self.collection = orders_collection

    def create_order(self, order: OrderCreate) -> OrderDB:
        order_dict = order.dict()
        new_order = OrderDB(**order_dict)
        self.collection.insert_one(new_order.dict())
        publish_order_created(new_order.dict())
        return new_order

    def get_order(self, order_id: str) -> Optional[OrderDB]:
        data = self.collection.find_one({"id": order_id})
        if data:
            return OrderDB(**data)
        return None

    def get_all_orders(self) -> List[OrderDB]:
        orders = self.collection.find()
        return [OrderDB(**order) for order in orders]

    def delete_order(self, order_id: str) -> bool:
        result = self.collection.delete_one({"id": order_id})
        return result.deleted_count == 1

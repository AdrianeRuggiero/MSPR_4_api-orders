from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4
from datetime import datetime


class OrderProduct(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)


class OrderBase(BaseModel):
    client_id: str
    products: List[OrderProduct]
    total_price: float = Field(..., gt=0)
    status: str = "pending"  # Exemple : "pending", "confirmed", "shipped", "cancelled"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OrderCreate(OrderBase):
    pass


class OrderDB(OrderBase):
    id: str = Field(default_factory=lambda: str(uuid4()))

    class Config:
        orm_mode = True

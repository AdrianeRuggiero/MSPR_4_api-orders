from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.order import OrderCreate, OrderDB
from app.services.order_service import OrderService
from app.db.mongo import orders_collection
from app.security.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

order_service = OrderService(orders_collection)


@router.post("/", response_model=OrderDB, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, user: dict = Depends(get_current_user)):
    return order_service.create_order(order)


@router.get("/", response_model=List[OrderDB])
def get_all_orders(user: dict = Depends(get_current_user)):
    return order_service.get_all_orders()


@router.get("/{order_id}", response_model=OrderDB)
def get_order(order_id: str, user: dict = Depends(get_current_user)):
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: str, user: dict = Depends(get_current_user)):
    success = order_service.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.schemas import OrderCreate, OrderRead
from app.models import User
from app.crud import (
    create_order,
    get_orders_by_user,
    get_order,
    delete_order,
)
from app.deps import get_db, get_current_user


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("", response_model=OrderRead, status_code=201)
def place_order(
    order_in: OrderCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        order = create_order(current_user.id, order_in, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return order


@router.get("", response_model=List[OrderRead])
def my_orders(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_orders_by_user(current_user.id, session)


@router.get("/{order_id}", response_model=OrderRead)
def get_order_endpoint(
    order_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = get_order(order_id, session)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}", status_code=204)
def cancel_order(
    order_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = get_order(order_id, session)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    delete_order(order_id, session)

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..database import engine
from ..schemas import OrderCreate, OrderRead
from ..crud import create_order, get_orders_by_user
from ..models import User
from ..deps import get_current_user


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


def get_db():
    with Session(engine) as session:
        yield session


@router.post("", response_model=OrderRead)
def place_order(
    order_in: OrderCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        order = create_order(current_user.id, order_in, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    items = [
        {
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price,
        }
        for item in order.items
    ]

    return {
        "id": order.id,
        "user_id": order.user_id,
        "total": order.total,
        "items": items,
    }


@router.get("", response_model=List[OrderRead])
def my_orders(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = get_orders_by_user(current_user.id, session)

    result = []
    for order in orders:
        items = [
            {
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price,
            }
            for item in order.items
        ]
        result.append(
            {
                "id": order.id,
                "user_id": order.user_id,
                "total": order.total,
                "items": items,
            }
        )

    return result


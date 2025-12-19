from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..schemas import ProductCreate, ProductRead
from ..models import User
from ..crud import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
)
from ..deps import get_db, get_current_user

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("", response_model=ProductRead, status_code=201)
def create_product_endpoint(
    product_in: ProductCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = create_product(product_in, session)
    return product


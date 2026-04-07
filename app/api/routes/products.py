from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.schemas import ProductCreate, ProductRead
from app.models import User
from app.crud import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
)
from app.deps import get_db, get_current_user

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
    return create_product(product_in, session)


@router.get("", response_model=List[ProductRead])
def list_products(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_db),
):
    return get_products(session, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductRead)
def get_product_endpoint(
    product_id: int,
    session: Session = Depends(get_db),
):
    product = get_product(product_id, session)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductRead)
def update_product_endpoint(
    product_id: int,
    product_in: ProductCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = update_product(product_id, product_in.dict(exclude_unset=True), session)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", status_code=204)
def delete_product_endpoint(
    product_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not delete_product(product_id, session):
        raise HTTPException(status_code=404, detail="Product not found")

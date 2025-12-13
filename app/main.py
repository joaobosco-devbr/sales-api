from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List
from .database import init_db, engine
from .models import Product, User
from .schemas import (
    ProductCreate, ProductRead, UserCreate, UserRead,
    Token, OrderCreate, OrderRead
)
from .crud import (
    create_user, get_user_by_username, create_product, get_products,
    get_product, update_product, delete_product, create_order, get_orders_by_user
)
from .auth import verify_password, create_access_token, decode_access_token
from sqlmodel import Session as _Session

app = FastAPI(title="Sales API")

@app.on_event("startup")
def on_startup():
    init_db()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    with _Session(engine) as session:
        yield session

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = get_user_by_username(username, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# Auth endpoints
@app.post("/signup", response_model=UserRead)
def signup(user_in: UserCreate, session: Session = Depends(get_db)):
    existing = get_user_by_username(user_in.username, session)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = create_user(user_in.username, user_in.password, session)
    return UserRead(id=user.id, username=user.username)

@app.post("/token", response_model=Token)
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    user = get_user_by_username(form_data.username, session)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Products CRUD (some routes protected for create/update/delete)
@app.post("/products", response_model=ProductRead)
def create_product_endpoint(product_in: ProductCreate, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    p = create_product(product_in, session)
    return ProductRead.from_orm(p)

@app.get("/products", response_model=List[ProductRead])
def list_products(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    return [ProductRead.from_orm(p) for p in get_products(session, skip, limit)]

@app.get("/products/{product_id}", response_model=ProductRead)
def read_product(product_id: int, session: Session = Depends(get_db)):
    p = get_product(product_id, session)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductRead.from_orm(p)

@app.patch("/products/{product_id}", response_model=ProductRead)
def patch_product(product_id: int, fields: dict, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    p = update_product(product_id, fields, session)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductRead.from_orm(p)

@app.delete("/products/{product_id}")
def remove_product(product_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ok = delete_product(product_id, session)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"ok": True}

# Orders
@app.post("/orders", response_model=OrderRead)
def place_order(order_in: OrderCreate, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        order = create_order(current_user.id, order_in, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # build response
    items = [{"id": it.id, "product_id": it.product_id, "quantity": it.quantity, "price": it.price} for it in order.items]
    return {"id": order.id, "user_id": order.user_id, "total": order.total, "items": items}

@app.get("/orders", response_model=List[OrderRead])
def my_orders(session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = get_orders_by_user(current_user.id, session)
    result = []
    for o in orders:
        items = [{"id": it.id, "product_id": it.product_id, "quantity": it.quantity, "price": it.price} for it in o.items]
        result.append({"id": o.id, "user_id": o.user_id, "total": o.total, "items": items})
    return result

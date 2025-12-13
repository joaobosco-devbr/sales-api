from typing import Optional, List
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# User
class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str

# Category
class CategoryCreate(BaseModel):
    name: str

class CategoryRead(CategoryCreate):
    id: int

# Product
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category_id: Optional[int] = None

class ProductRead(ProductCreate):
    id: int

# Order
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

class OrderRead(BaseModel):
    id: int
    user_id: int
    total: float
    items: List[OrderItemRead]

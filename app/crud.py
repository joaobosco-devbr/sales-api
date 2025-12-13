from sqlmodel import Session, select
from .models import User, Product, Category, Order, OrderItem
from .schemas import ProductCreate, OrderCreate, OrderItemCreate
from .auth import get_password_hash
from .database import engine

def create_user(username: str, password: str, session: Session):
    user = User(username=username, hashed_password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_username(username: str, session: Session):
    return session.exec(select(User).where(User.username == username)).first()

# Category
def create_category(name: str, session: Session):
    category = Category(name=name)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

# Product
def create_product(product_in: ProductCreate, session: Session):
    product = Product.from_orm(product_in)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def get_products(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Product).offset(skip).limit(limit)).all()

def get_product(product_id: int, session: Session):
    return session.get(Product, product_id)

def update_product(product_id: int, fields: dict, session: Session):
    product = session.get(Product, product_id)
    if not product:
        return None
    for k, v in fields.items():
        setattr(product, k, v)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def delete_product(product_id: int, session: Session):
    p = session.get(Product, product_id)
    if not p:
        return False
    session.delete(p)
    session.commit()
    return True

# Orders
def create_order(user_id: int, order_in: OrderCreate, session: Session):
    order = Order(user_id=user_id, total=0.0)
    session.add(order)
    session.commit()
    session.refresh(order)

    total = 0.0
    for item in order_in.items:
        product = session.get(Product, item.product_id)
        if not product or product.stock < item.quantity:
            raise ValueError(f"Product {item.product_id} not available or insufficient stock")
        price = product.price
        order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, price=price)
        session.add(order_item)
        product.stock -= item.quantity
        total += price * item.quantity

    order.total = total
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def get_orders_by_user(user_id: int, session: Session):
    return session.exec(select(Order).where(Order.user_id == user_id)).all()

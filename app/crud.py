from sqlmodel import Session, select

from app.models import (
    User,
    Category,
    Product,
    Order,
    OrderItem,
)
from app.schemas import (
    ProductCreate,
    OrderCreate,
    OrderItemCreate,
)
from app.auth import get_password_hash


# =========================
# USERS
# =========================

def create_user(username: str, password: str, session: Session):
    user = User(
        username=username,
        hashed_password=get_password_hash(password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(username: str, session: Session):
    return session.exec(
        select(User).where(User.username == username)
    ).first()


# =========================
# CATEGORIES
# =========================

def create_category(name: str, session: Session):
    category = Category(name=name)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def get_categories(session: Session):
    return session.exec(select(Category)).all()


# =========================
# PRODUCTS
# =========================

def create_product(product_in: ProductCreate, session: Session):
    product = Product.from_orm(product_in)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def get_products(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(
        select(Product).offset(skip).limit(limit)
    ).all()


def get_product(product_id: int, session: Session):
    return session.get(Product, product_id)


def update_product(product_id: int, fields: dict, session: Session):
    product = session.get(Product, product_id)
    if not product:
        return None

    for key, value in fields.items():
        setattr(product, key, value)

    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def delete_product(product_id: int, session: Session):
    product = session.get(Product, product_id)
    if not product:
        return False

    session.delete(product)
    session.commit()
    return True


# =========================
# ORDERS
# =========================

def create_order(user_id: int, order_in: OrderCreate, session: Session):
    total = 0.0
    items_data = []

    for item in order_in.items:
        product = session.get(Product, item.product_id)
        if not product:
            raise ValueError(f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise ValueError(
                f"Insufficient stock for product '{product.name}': "
                f"requested {item.quantity}, available {product.stock}"
            )
        total += product.price * item.quantity
        items_data.append((product, item.quantity, product.price))

    order = Order(user_id=user_id, total=round(total, 2))
    session.add(order)
    session.flush()

    for product, quantity, price in items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            price=price,
        )
        session.add(order_item)
        product.stock -= quantity
        session.add(product)

    session.commit()
    session.refresh(order)
    return order


def get_orders(session: Session):
    return session.exec(select(Order)).all()


def get_orders_by_user(user_id: int, session: Session):
    return session.exec(
        select(Order).where(Order.user_id == user_id)
    ).all()


def get_order(order_id: int, session: Session):
    return session.get(Order, order_id)


def delete_order(order_id: int, session: Session):
    order = session.get(Order, order_id)
    if not order:
        return False

    session.delete(order)
    session.commit()
    return True


# =========================
# ORDER ITEMS
# =========================

def create_order_item(
    order_item_in: OrderItemCreate,
    session: Session
):
    item = OrderItem.from_orm(order_item_in)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def get_order_items(order_id: int, session: Session):
    return session.exec(
        select(OrderItem).where(OrderItem.order_id == order_id)
    ).all()

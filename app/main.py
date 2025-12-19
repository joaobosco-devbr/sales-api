from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from .database import init_db
from .models import User
from .schemas import UserCreate, UserRead, Token
from .crud import create_user, get_user_by_username
from .auth import verify_password, create_access_token
from .deps import get_db, get_current_user

from .routers import products, orders


app = FastAPI(title="Sales API")


@app.on_event("startup")
def on_startup():
    init_db()


# ---------------- ROUTERS ----------------

app.include_router(products.router)
app.include_router(orders.router)


# ---------------- AUTH ----------------

@app.post("/signup", response_model=UserRead, status_code=201)
def signup(
    user_in: UserCreate,
    session: Session = Depends(get_db),
):
    existing = get_user_by_username(user_in.username, session)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    user = create_user(user_in.username, user_in.password, session)
    return UserRead(id=user.id, username=user.username)


@app.post("/token", response_model=Token)
def login_for_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
):
    user = get_user_by_username(form_data.username, session)

    if not user or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect credentials",
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from .database import engine
from .crud import get_user_by_username
from .auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    with Session(engine) as session:
        yield session


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = get_user_by_username(username, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


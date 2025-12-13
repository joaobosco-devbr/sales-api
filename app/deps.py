from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from .database import engine
from .auth import decode_access_token
from .crud import get_user_by_username

def get_session():
    with Session(engine) as session:
        yield session

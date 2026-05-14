from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.auth import get_current_user
from app.models import UserDB


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_admin(
    current_user: UserDB = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user
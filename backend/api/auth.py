import re
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import User
from backend.db.schemas import UserRegister, UserLogin, Token
from backend.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from backend.core.rate_limiter import rate_limit

router = APIRouter(prefix="", tags=["Authentication"])


def validate_password_complexity(password: str):
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long."
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one uppercase letter."
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one lowercase letter."
        )
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one numeric digit."
        )


@router.post("/register", status_code=status.HTTP_201_CREATED, dependencies=[Depends(rate_limit)])
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or Username is already registered."
        )

    validate_password_complexity(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Registration Successful",
        "user_id": new_user.id,
        "username": new_user.username
    }


@router.post("/login", response_model=Token, dependencies=[Depends(rate_limit)])
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == user_credentials.email
    ).first()

    if not db_user or not verify_password(user_credentials.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        data={"sub": db_user.email, "username": db_user.username, "user_id": db_user.id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
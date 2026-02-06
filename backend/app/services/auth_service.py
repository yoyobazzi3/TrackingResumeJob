from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import hash_password, verify_password


def create_user(db: Session, email: str, password: str):
    email = email.lower().strip()

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    user = User(
        email=email,
        hashed_password=hash_password(password),
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    email = email.lower().strip()

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user

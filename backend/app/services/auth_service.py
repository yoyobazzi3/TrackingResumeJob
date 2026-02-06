"""Auth service layer for user creation and authentication."""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import hash_password, verify_password


def create_user(
    db: Session,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
):
    """
    Create a new user account.

    - Normalizes email
    - Hashes password
    - Stores first and last name
    """
    email = email.lower().strip()

    # Check for existing user.
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        hashed_password=hash_password(password),
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Handle unique constraint race conditions.
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user by email and password.
    """
    email = email.lower().strip()

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user

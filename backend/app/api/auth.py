from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import SignupRequest, LoginRequest
from app.services.auth_service import create_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    user = create_user(db, payload.email, payload.password)
    return {
        "id": str(user.id),
        "email": user.email
    }


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return {
        "id": str(user.id),
        "email": user.email
    }

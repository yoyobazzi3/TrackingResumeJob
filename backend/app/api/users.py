"""User-related API routes."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    # Return the authenticated user's profile.
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
    }


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete the currently authenticated user.
    Intended for development/testing only.
    """
    db.delete(current_user)
    db.commit()

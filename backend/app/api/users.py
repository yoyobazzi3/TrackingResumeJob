from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
    }

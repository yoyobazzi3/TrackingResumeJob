"""Simple health-check endpoint."""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
def health_check():
    # Basic liveness response.
    return {"status": "healthy"}

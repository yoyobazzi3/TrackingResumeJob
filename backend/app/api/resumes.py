# app/api/resumes.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.schemas.resume import (
    ResumeCreateRequest,
    ResumeResponse,
    ResumeListResponse,
)
from app.models.user import User
from app.services import resume_service

router = APIRouter(prefix="/resumes", tags=["resumes"])

@router.post(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_resume(
    payload: ResumeCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return resume_service.create_resume(
        db,
        user_id=current_user.id,
        content=payload.content,
    )


@router.get("", response_model=list[ResumeListResponse])
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return resume_service.list_resumes(
        db,
        user_id=current_user.id,
    )


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return resume_service.get_resume(
        db,
        resume_id=resume_id,
        user_id=current_user.id,
    )


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume_service.delete_resume(
        db,
        resume_id=resume_id,
        user_id=current_user.id,
    )

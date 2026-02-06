# app/services/resume_service.py

from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status

from app.repositories import resume_repository


def create_resume(db: Session, *, user_id: str, content: dict):
    return resume_repository.create(
        db,
        user_id=user_id,
        content=content,
    )


def list_resumes(db: Session, *, user_id: str):
    return resume_repository.get_all_for_user(
        db,
        user_id=user_id,
    )


def get_resume(db: Session, *, resume_id: UUID, user_id: str):
    resume = resume_repository.get_by_id(
        db,
        resume_id=resume_id,
        user_id=user_id,
    )

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    return resume


def delete_resume(db: Session, *, resume_id: UUID, user_id: str):
    resume = get_resume(
        db,
        resume_id=resume_id,
        user_id=user_id,
    )

    if resume.is_frozen:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Frozen resumes cannot be deleted",
        )

    resume_repository.delete(db, resume=resume)

# app/repositories/resume_repository.py

from sqlalchemy.orm import Session
from uuid import UUID
from app.models.resume import Resume


def create(db: Session, *, user_id: str, content: dict) -> Resume:
    resume = Resume(
        user_id=user_id,
        content=content,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def get_all_for_user(db: Session, *, user_id: str) -> list[Resume]:
    return (
        db.query(Resume)
        .filter(Resume.user_id == user_id)
        .order_by(Resume.created_at.desc())
        .all()
    )


def get_by_id(db: Session, *, resume_id: UUID, user_id: str) -> Resume | None:
    return (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == user_id,
        )
        .first()
    )


def delete(db: Session, *, resume: Resume) -> None:
    db.delete(resume)
    db.commit()

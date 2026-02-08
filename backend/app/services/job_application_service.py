from sqlalchemy.orm import Session
from uuid import UUID

from app.models.job_application import JobApplication
from app.schemas.job_application import JobApplicationCreate, ApplicationStatus

_UNSET = object()


def create_job_application(
    db: Session,
    *,
    user_id: UUID,
    data: JobApplicationCreate,
) -> JobApplication:
    app = JobApplication(
        user_id=user_id,
        company=data.company,
        role=data.role,
        status=data.status,
        resume_id=data.resume_id,
        job_description=data.job_description,
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


def get_job_applications(
    db: Session,
    *,
    user_id: UUID,
) -> list[JobApplication]:
    return (
        db.query(JobApplication)
        .filter(JobApplication.user_id == user_id)
        .order_by(JobApplication.created_at.desc())
        .all()
    )


def get_job_application(
    db: Session,
    *,
    user_id: UUID,
    application_id: UUID,
) -> JobApplication | None:
    return (
        db.query(JobApplication)
        .filter(
            JobApplication.id == application_id,
            JobApplication.user_id == user_id,
        )
        .first()
    )


def delete_job_application(
    db: Session,
    *,
    user_id: UUID,
    application_id: UUID,
) -> bool:
    app = get_job_application(
        db,
        user_id=user_id,
        application_id=application_id,
    )
    if not app:
        return False

    db.delete(app)
    db.commit()
    return True


def update_job_application(
    db: Session,
    *,
    user_id: UUID,
    application_id: UUID,
    status: ApplicationStatus | None | object = _UNSET,
    resume_id: UUID | None | object = _UNSET,
    job_description: str | None | object = _UNSET,
) -> JobApplication | None:
    app = get_job_application(
        db,
        user_id=user_id,
        application_id=application_id,
    )
    if not app:
        return None

    if status is not _UNSET:
        app.status = status

    if resume_id is not _UNSET:
        app.resume_id = resume_id

    if job_description is not _UNSET:
        app.job_description = job_description

    db.commit()
    db.refresh(app)
    return app

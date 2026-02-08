from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.job_application import (
    JobApplicationCreate,
    JobApplicationRead,
    JobApplicationUpdate,
)
from app.services.job_application_service import (
    create_job_application,
    get_job_applications,
    get_job_application,
    delete_job_application,
    update_job_application,
)
from app.services.keyword_match_service import compute_keyword_match
from app.services.ats_match_engine import ats_score

router = APIRouter(prefix="/job-applications", tags=["job-applications"])


@router.post(
    "",
    response_model=JobApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_job_application(
        db,
        user_id=current_user.id,
        data=data,
    )


@router.get("", response_model=list[JobApplicationRead])
def list_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_job_applications(
        db,
        user_id=current_user.id,
    )


@router.get("/{application_id}", response_model=JobApplicationRead)
def get_one(
    application_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app = get_job_application(
        db,
        user_id=current_user.id,
        application_id=application_id,
    )
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    application_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ok = delete_job_application(
        db,
        user_id=current_user.id,
        application_id=application_id,
    )
    if not ok:
        raise HTTPException(status_code=404, detail="Application not found")


@router.patch("/{application_id}", response_model=JobApplicationRead)
def update(
    application_id: UUID,
    data: JobApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    payload = data.model_dump(exclude_unset=True)
    app = update_job_application(
        db,
        user_id=current_user.id,
        application_id=application_id,
        **payload,
    )
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


@router.get("/{application_id}/keyword-match")
def keyword_match(
    application_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app = get_job_application(
        db,
        user_id=current_user.id,
        application_id=application_id,
    )
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    result = compute_keyword_match(app)
    if result is None:
        return {
            "score": 0,
            "matched": [],
            "missing": [],
            "total_keywords": 0,
        }

    return result


@router.get("/{application_id}/ats-score")
def ats_analysis(
    application_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app = get_job_application(
        db,
        user_id=current_user.id,
        application_id=application_id,
    )
    if not app or not app.job_description or not app.resume:
        return {
            "overall_score": 0,
            "strong_matches": [],
            "weak_matches": [],
            "missing_critical": [],
            "evidence": {},
        }

    return ats_score(app.job_description, app.resume.content)

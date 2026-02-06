"""Job application model for tracking application status."""

import enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, ForeignKey
from app.core.database import Base
from app.models.base import UUIDBase

class ApplicationStatus(enum.Enum):
    # Allowed states of an application.
    saved = "saved"
    applied = "applied"
    oa = "oa"
    interview = "interview"
    rejected = "rejected"

class JobApplication(UUIDBase, Base):
    __tablename__ = "job_applications"

    # Applicant user.
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    # Resume used for this application.
    resume_id: Mapped[str] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=False,
    )

    # Company name.
    company: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # Role/title applied for.
    role: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # Current status of the application.
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.saved,
        nullable=False,
    )

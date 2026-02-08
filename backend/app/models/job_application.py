"""Job application model for tracking application status."""

import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, ForeignKey, Text

from app.core.database import Base
from app.models.base import UUIDBase


class ApplicationStatus(enum.Enum):
    saved = "saved"
    applied = "applied"
    oa = "oa"
    interview = "interview"
    rejected = "rejected"


class JobApplication(UUIDBase, Base):
    __tablename__ = "job_applications"

    # Applicant user
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Resume used (optional)
    resume_id: Mapped[str | None] = mapped_column(
        ForeignKey("resumes.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Company name
    company: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # Role/title applied for
    role: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # Application status
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="applicationstatus"),
        nullable=False,
        default=ApplicationStatus.saved,
    )

    # Raw job description (important later for AI)
    job_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    user = relationship("User", back_populates="job_applications")
    resume = relationship("Resume", back_populates="job_applications")

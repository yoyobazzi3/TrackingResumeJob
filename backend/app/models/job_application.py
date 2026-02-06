import enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, ForeignKey
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

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    resume_id: Mapped[str] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=False,
    )

    company: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.saved,
        nullable=False,
    )

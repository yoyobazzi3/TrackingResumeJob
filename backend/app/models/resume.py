"""Resume model representing a user's resume snapshot."""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import ForeignKey
from app.core.database import Base
from app.models.base import UUIDBase

class Resume(UUIDBase, Base):
    __tablename__ = "resumes"

    # Owner of this resume.
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    # Resume content stored as JSON.
    content: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    # Frozen resumes are not modified by later edits.
    is_frozen: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
    
    job_applications = relationship(
        "JobApplication",
        back_populates="resume",
    )

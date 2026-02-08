"""User model."""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from app.core.database import Base
from app.models.base import UUIDBase


class User(UUIDBase, Base):
    __tablename__ = "users"

    # Unique user email.
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    # User identity
    first_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # Auth
    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # Account state
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    job_applications = relationship(
        "JobApplication",
        back_populates="user",
        cascade="all, delete-orphan",
    )

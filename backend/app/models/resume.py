from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import ForeignKey
from app.core.database import Base
from app.models.base import UUIDBase

class Resume(UUIDBase, Base):
    __tablename__ = "resumes"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    content: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    is_frozen: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

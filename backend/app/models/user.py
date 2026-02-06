from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.core.database import Base
from app.models.base import UUIDBase

class User(UUIDBase, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

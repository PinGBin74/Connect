from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models import Base


class UserProfile(Base):
    __tablename__ = "UserProfile"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    photo: Mapped[str] = mapped_column(String)

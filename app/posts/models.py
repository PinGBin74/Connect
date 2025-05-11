from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime
from app.infrastructure.database.models import Base


class Posts(Base):
    __tablename__ = "Posts"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    username: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfile.id"), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    photo_url: Mapped[Optional[str]] = mapped_column(nullable=True)

    def __repr__(self):
        return f"<Post(id={self.id}, username={self.username}, created_at={self.created_at}, content={self.content[:20]}...)>"

    def serialize_created_at(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.models import Base


class UserSettings(Base):
    __tablename__ = "UserSettings"

    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfile.id"), primary_key=True)
    delete_photo_after_days: Mapped[bool] = mapped_column(Boolean, default=True)

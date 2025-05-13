from typing import Optional, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models import Base
from app.users.subscription.models import subscriptions


class UserProfile(Base):
    __tablename__ = "UserProfile"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)

    following: Mapped[List["UserProfile"]] = relationship(
        "UserProfile",
        secondary=subscriptions,
        primaryjoin="UserProfile.id==subscriptions.c.follower_id",
        secondaryjoin="UserProfile.id==subscriptions.c.following_id",
        back_populates="followers",
    )

    followers: Mapped[List["UserProfile"]] = relationship(
        "UserProfile",
        secondary=subscriptions,
        primaryjoin="UserProfile.id==subscriptions.c.following_id",
        secondaryjoin="UserProfile.id==subscriptions.c.follower_id",
        back_populates="following",
    )

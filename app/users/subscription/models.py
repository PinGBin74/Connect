from sqlalchemy import Column, ForeignKey, Table

from app.infrastructure.database.models import Base


subscriptions = Table(
    "subscriptions",
    Base.metadata,
    Column("follower_id", ForeignKey("UserProfile.id"), primary_key=True),
    Column("following_id", ForeignKey("UserProfile.id"), primary_key=True),
)

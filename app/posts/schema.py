import datetime
from pydantic import BaseModel, field_serializer, model_validator


class PostSchema(BaseModel):
    id: int | None = None
    created_at: datetime.datetime | None = None
    username: str | None = None
    user_id: int | None = None
    content: str | None = None
    photo_url: str | None = None

    class Config:
        from_attributes = True

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime.datetime | None) -> str | None:
        if created_at is None:
            return None
        return created_at.strftime("%Y-%m-%d %H:%M:%S")

    @model_validator(mode="after")
    def check_content_is_not_none(self):
        if self.content is None:
            raise ValueError("content must be provided")
        return self


class PostCreateSchema(BaseModel):
    content: str
    photo_url: str | None = None

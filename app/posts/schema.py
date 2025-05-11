from pydantic import BaseModel, model_validator


class PostSchema(BaseModel):
    username: str | None
    user_id: str | None
    title: str | None
    content: str | None

    class Config:
        from_attributes = True

    @model_validator(model="after")
    def check_title_or_content_is_not_none(self):
        if self.title is None and self.content is None:
            raise ValueError("title or content must be provided")


class PostCreateSchema(BaseModel):
    title: str | None
    content: str | None

from pydantic import BaseModel

from app.posts.schema import PostSchema


class SubscriptionCreate(BaseModel):
    username: str


class SubscriptionResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class SubscriptionMessageResponse(BaseModel):
    message: str


class SubscriptionPostsResponse(PostSchema):
    pass

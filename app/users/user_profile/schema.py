from typing import Optional
from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    photo_url: Optional[str] = None

    class Config:
        from_attributes = True

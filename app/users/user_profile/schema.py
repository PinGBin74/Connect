from typing import Optional
from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True

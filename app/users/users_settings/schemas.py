from pydantic import BaseModel


class UserSettingsRequest(BaseModel):
    delete_photo_after_days: bool

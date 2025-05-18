from fastapi import APIRouter, Depends, Query

from app.dependecy import get_settings_service, get_current_user_id
from app.users.users_settings.service import UserSettingsService


router = APIRouter(prefix="/settings", tags=["settings"])


@router.post("", response_model=bool)
async def update_settings(
    delete_photo_after_days: bool = Query(
        ..., description="Choose whether to delete photos after days"
    ),
    user_settings_service: UserSettingsService = Depends(get_settings_service),
    user_id: int = Depends(get_current_user_id),
) -> bool:
    result = await user_settings_service.update_settings(
        user_id=user_id, delete_photo_after_days=delete_photo_after_days
    )
    return result

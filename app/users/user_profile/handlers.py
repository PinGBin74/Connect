from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form

from app.dependecy import get_user_service

from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.schema import UserCreateSchema
from app.users.user_profile.service import UserService
from app.yandex_disk.service import YandexDiskService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserLoginSchema)
async def create_user(
    user_service: Annotated[UserService, Depends(get_user_service)],
    storage: Annotated[YandexDiskService, Depends(lambda: YandexDiskService())],
    username: str = Form(...),
    password: str = Form(...),
    photo: UploadFile = File(None),
):
    photo_url = None
    if photo is not None:
        file_extension = photo.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        photo_url = await storage.upload_file(photo.file, filename)
    user_data = UserCreateSchema(username=username, password=password, photo_url=photo_url)
    return await user_service.create_user_with_photo(user_data)

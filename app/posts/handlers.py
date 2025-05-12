from typing import Annotated
import uuid
from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File, Form

from app.dependecy import get_post_service, get_request_user_id
from app.exception import PostNotFound
from app.posts.schema import PostCreateSchema, PostSchema
from app.posts.service import PostService
from app.yandex_disk.service import YandexDiskService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/all", response_model=list[PostSchema])
async def get_posts(
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    posts = await post_service.get_posts()
    return posts


@router.post("/", response_model=PostSchema)
async def create_post(
    post_service: Annotated[PostService, Depends(get_post_service)],
    user_id: int = Depends(get_request_user_id),
    content: str = Form(...),
    photo: UploadFile = File(None),
    storage: YandexDiskService = Depends(lambda: YandexDiskService()),
):
    photo_url = None
    if photo:
        file_extension = photo.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        photo_url = await storage.upload_file(photo.file, filename)
    post_data = PostCreateSchema(content=content, photo_url=photo_url)
    post = await post_service.create_post(post_data, user_id)
    return post


@router.patch(
    "/{post_id}",
    response_model=PostSchema,
)
async def patch_post(
    post_id: int,
    content: str,
    post_service: Annotated[PostService, Depends(get_post_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        return await post_service.update_post_name(
            post_id=post_id, content=content, user_id=user_id
        )
    except PostNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    post_service: Annotated[PostService, Depends(get_post_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        await post_service.delete_post(post_id=post_id, user_id=user_id)
    except PostNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)

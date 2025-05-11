from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from app.dependecy import get_post_service, get_request_user_id
from app.exception import PostNotFound
from app.posts.schema import PostCreateSchema, PostSchema
from app.posts.service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/all", response_model=list[PostSchema])
async def get_posts(
    post_service: Annotated[PostService, Depends(get_post_service)],
):
    posts = await post_service.get_posts()
    return posts


@router.post("/", response_model=PostSchema)
async def create_post(
    body: PostCreateSchema,
    post_service: Annotated[PostService, Depends(get_post_service)],
    user_id: int = Depends(get_request_user_id),
):
    post = await post_service.create_post(body, user_id)
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

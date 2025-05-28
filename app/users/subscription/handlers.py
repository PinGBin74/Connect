from fastapi import APIRouter, Depends
from app.users.subscription.schema import (
    SubscriptionCreate,
    SubscriptionResponse,
    SubscriptionPostsResponse,
    SubscriptionMessageResponse,
)
from app.users.subscription.service import SubscripionService
from app.dependecy import get_request_user_id, get_subscription_service


router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.post("", status_code=201, response_model=SubscriptionMessageResponse)
async def create_subscription(
    subscription_data: SubscriptionCreate,
    follower_id: int = Depends(get_request_user_id),
    subscription_service: SubscripionService = Depends(get_subscription_service),
) -> SubscriptionMessageResponse:
    success = await subscription_service.subscribe(
        subscription_data=subscription_data,
        follower_id=follower_id,
    )
    if not success:
        return SubscriptionMessageResponse(
            message=f"You subscribed to {subscription_data.username}"
        )
    return SubscriptionMessageResponse(message="Failed to subcribe")


@router.delete("", response_model=SubscriptionMessageResponse)
async def delete_subscription(
    subscription_data: SubscriptionCreate,
    follower_id: int = Depends(get_request_user_id),
    subscription_service: SubscripionService = Depends(get_subscription_service),
) -> SubscriptionMessageResponse:
    success = await subscription_service.unsubscribe(
        subscription_data=subscription_data,
        follower_id=follower_id,
    )
    if not success:
        return SubscriptionMessageResponse(
            message=f"Вы отписались от пользователя {subscription_data.username}"
        )
    return SubscriptionMessageResponse(message="Не удалось отписаться от пользователя")


@router.get("/following", response_model=list[SubscriptionResponse])
async def get_following(
    follower_id: int = Depends(get_request_user_id),
    subscription_service: SubscripionService = Depends(get_subscription_service),
) -> list[SubscriptionResponse]:
    return await subscription_service.get_following(follower_id=follower_id)


@router.get("/posts", response_model=list[SubscriptionPostsResponse])
async def get_following_posts(
    follower_id: int = Depends(get_request_user_id),
    subscription_service: SubscripionService = Depends(get_subscription_service),
) -> list[SubscriptionPostsResponse]:
    return await subscription_service.get_following_posts(follower_id=follower_id)


@router.get("/folowers", response_model=list[SubscriptionResponse])
async def get_followers(
    follower_id: int = Depends(get_request_user_id),
    subscription_service: SubscripionService = Depends(get_subscription_service),
) -> list[SubscriptionResponse]:
    return await subscription_service.get_followers(follower_id=follower_id)

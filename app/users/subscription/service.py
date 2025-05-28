from dataclasses import dataclass
from app.users.subscription.repository import SubscriptionRepository
from app.users.subscription.schema import (
    SubscriptionCreate,
    SubscriptionPostsResponse,
    SubscriptionResponse,
)


@dataclass
class SubscripionService:
    subscription_repository: SubscriptionRepository

    async def subscribe(
        self, subscription_data: SubscriptionCreate, follower_id: int
    ) -> None:
        await self.subscription_repository.subscribe(
            follower_id=follower_id, followed_username=subscription_data.username
        )

    async def unsubscribe(
        self, subscription_data: SubscriptionCreate, follower_id: int
    ) -> None:
        await self.subscription_repository.unsubscribe(
            follower_id=follower_id, followed_username=subscription_data.username
        )

    async def get_following(self, follower_id: int) -> list[SubscriptionResponse]:
        return await self.subscription_repository.get_following(follower_id=follower_id)

    async def get_following_posts(
        self, follower_id: int
    ) -> list[SubscriptionPostsResponse]:
        return await self.subscription_repository.get_following_posts(
            follower_id=follower_id
        )

    async def get_followers(self, follower_id: int) -> list[SubscriptionResponse]:
        return await self.subscription_repository.get_followers(follower_id=follower_id)

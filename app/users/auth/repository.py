import json
from typing import Optional
from redis import Redis

from app.users.user_profile.schema import UserCreateSchema



class UserCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_user_profile(self, user_id: int) -> Optional[UserCreateSchema]:
        """Get profile by id"""
        async with self.redis as redis:
            user_json = await redis.get(f"user:{user_id}")
            if user_json:
                return UserCreateSchema.model_validate(json.loads(user_json))
            return None

    async def set_user_profile(self, user_id: int, user_data: UserCreateSchema):
        """Save profile's email"""
        user_json = user_data.model_dump_json()
        async with self.redis as redis:
            await redis.set(f"user:{user_id}", user_json)

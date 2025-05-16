from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.posts.models import Posts
import datetime as dt


class PostRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def delete_old_posts(self, hours: int = 1) -> int:
        """
        Delete posts older than the specified number of hours
        :param hours: Quantity of hours
        :return: Quantity of deleted posts
        """
        query = delete(Posts).where(
            Posts.created_at < dt.datetime.utcnow() - dt.timedelta(hours=hours)
        )
        result = await self.db_session.execute(query)
        await self.db_session.commit()
        return result.rowcount

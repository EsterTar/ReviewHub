from functools import lru_cache
from uuid import UUID
from pymongo.errors import DuplicateKeyError
from schemas.likes import Like

import config

settings = config.get_settings()


class LikeService:

    def __init__(self):
        self.model = Like

    async def create_like(
            self,
            user_id: UUID,
            movie_id: UUID,
            rating: int
    ) -> Like:
        like = self.model(
            user_id=user_id,
            movie_id=movie_id,
            rating=rating
        )
        await like.insert()
        return like

    async def get_like(self, like_id: UUID) -> Like:
        like = await self.model.get(document_id=like_id)
        return like

    async def get_likes_list(
            self,
            skip: int = 0,
            limit: int = 10,
            user_id: UUID = None,
            movie_id: UUID = None,
    ):
        filters = {}
        if user_id:
            filters['user_id'] = user_id
        if movie_id:
            filters['movie_id'] = movie_id

        likes = await self.model.find(filters).skip(skip).limit(limit).to_list()
        count = await self.model.find(filters).count()
        return likes, count


@lru_cache()
def get_like_service() -> LikeService:
    return LikeService()

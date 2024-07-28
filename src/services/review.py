from functools import lru_cache
from uuid import UUID
from schemas.reviews import Review

import config

settings = config.get_settings()


class ReviewService:

    def __init__(self):
        self.model = Review

    async def create_review(
            self,
            user_id: UUID,
            movie_id: UUID,
            text: str,
            user_rating: int,
            likes: int = 0,
            dislikes: int = 0,
    ) -> Review:
        review = self.model(
            user_id=user_id,
            movie_id=movie_id,
            text=text,
            likes=likes,
            dislikes=dislikes,
            user_rating=user_rating,
        )
        await review.insert()
        return review

    async def get_review(self, review_id: UUID) -> Review:
        review = await self.model.get(document_id=review_id)
        return review

    async def get_reviews_list(
            self,
            skip: int = 0,
            limit: int = 10,
            user_id: UUID = None,
            movie_id: UUID = None,
            user_rating: int = None
    ):
        filters = {}
        if user_id is not None:
            filters["user_id"] = user_id
        if movie_id is not None:
            filters["movie_id"] = movie_id
        if user_rating is not None:
            filters["user_rating"] = user_rating

        reviews = await self.model.find(filters).skip(skip).limit(limit).to_list()
        count = await self.model.find(filters).count()
        return reviews, count


@lru_cache()
def get_review_service() -> ReviewService:
    return ReviewService()

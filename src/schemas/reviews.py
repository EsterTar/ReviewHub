from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field, BaseModel
from pymongo import IndexModel, ASCENDING

from schemas.common import Meta


class Review(Document):
    id: UUID = Field(default_factory=uuid4)
    user_id: Annotated[UUID, Indexed()]
    movie_id: Annotated[UUID, Indexed()]
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    likes: int = Field(default=0)
    dislikes: int = Field(default=0)
    user_rating: int = Field(..., ge=0, le=10)

    class Settings:
        collection = "reviews"
        indexes = [
            IndexModel([("user_id", ASCENDING), ("movie_id", ASCENDING)], name="user_movie_idx", unique=True)
        ]


class CreateReviewRequest(BaseModel):
    user_id: UUID
    movie_id: UUID
    text: str
    likes: int = Field(default=0)
    dislikes: int = Field(default=0)
    user_rating: int = Field(..., ge=0, le=10)


class GetReviewsListResponse(BaseModel):
    data: list[Review]
    meta: Meta

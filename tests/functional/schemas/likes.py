from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field, BaseModel
from pymongo import IndexModel, ASCENDING

from schemas.common import Meta


class Like(Document):
    id: UUID = Field(default_factory=uuid4)
    user_id: Annotated[UUID, Indexed()]
    movie_id: Annotated[UUID, Indexed()]
    rating: int = Field(..., ge=0, le=10)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        collection = "likes"
        indexes = [
            IndexModel([("user_id", ASCENDING), ("movie_id", ASCENDING)], name="user_movie_idx", unique=True)
        ]


class CreateLikeRequest(BaseModel):
    user_id: UUID
    movie_id: UUID
    rating: int


class GetLikesListResponse(BaseModel):
    data: list[Like]
    meta: Meta

from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field, BaseModel
from pymongo import ASCENDING, IndexModel

from schemas.common import Meta


class Bookmark(Document):
    id: UUID = Field(default_factory=uuid4)
    user_id: Annotated[UUID, Indexed()]
    movie_id: Annotated[UUID, Indexed()]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        collection = "bookmarks"
        indexes = [
            IndexModel([("user_id", ASCENDING), ("movie_id", ASCENDING)], name="user_movie_idx", unique=True)
        ]


class CreateBookmarkRequest(BaseModel):
    user_id: UUID
    movie_id: UUID


class GetBookmarksListResponse(BaseModel):
    data: list[Bookmark]
    meta: Meta

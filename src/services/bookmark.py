from functools import lru_cache
from uuid import UUID
from pymongo.errors import DuplicateKeyError
from schemas.bookmarks import Bookmark

import config

settings = config.get_settings()


class BookmarkService:

    def __init__(self):
        self.model = Bookmark

    async def create_bookmark(
            self,
            user_id: UUID,
            movie_id: UUID,
    ) -> Bookmark:
        bookmark = self.model(
            user_id=user_id,
            movie_id=movie_id
        )
        await bookmark.insert()
        return bookmark

    async def get_bookmark(self, bookmark_id: UUID) -> Bookmark:
        bookmark = await self.model.get(document_id=bookmark_id)
        return bookmark

    async def get_bookmarks_list(
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

        bookmarks = await self.model.find(filters).skip(skip).limit(limit).to_list()
        count = await self.model.find(filters).count()
        return bookmarks, count


@lru_cache()
def get_bookmark_service() -> BookmarkService:
    return BookmarkService()

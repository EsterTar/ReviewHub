from functional.schemas.bookmarks import Bookmark
from functional.schemas.likes import Like
from functional.schemas.reviews import Review

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from functional import config
settings = config.get_settings()


class MongoClient:

    @classmethod
    async def get(cls) -> AsyncIOMotorClient:
        client = AsyncIOMotorClient(
            f'mongodb://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}'
        )
        await init_beanie(
            database=client.get_database(settings.db_name),
            document_models=[Like, Review, Bookmark],
            allow_index_dropping=True
        )
        return client

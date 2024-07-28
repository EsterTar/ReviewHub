import uvicorn
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager

from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from starlette import status

from api.v1 import likes, bookmarks, reviews
from beanie import init_beanie

import config
from schemas.bookmarks import Bookmark
from schemas.likes import Like
from schemas.reviews import Review

from motor.motor_asyncio import AsyncIOMotorClient

settings = config.get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    client = AsyncIOMotorClient(
        f'mongodb://{settings.mongodb_uri}'
    )
    await init_beanie(
        database=client.get_database(settings.db_name),
        document_models=[Like, Review, Bookmark],
        allow_index_dropping=True
    )
    yield
    client.close()


sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = FastAPI(
    title=settings.app_name,
    version='1.0',
    # docs_url='/docs',
    # openapi_url='/docs/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


@app.middleware('http')
async def before_request(request: Request, call_next):
    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    if not request_id and not settings.debug:
        return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'})
    return response

app.add_middleware(ServerErrorMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(reviews.router, prefix='/api/v1/reviews', tags=['reviews'])
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['bookmarks'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.app_host,
        port=settings.app_port,
    )

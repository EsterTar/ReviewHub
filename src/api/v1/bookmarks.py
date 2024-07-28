from uuid import UUID

from starlette import status as http_status
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.bookmarks import Bookmark, CreateBookmarkRequest, GetBookmarksListResponse
from services.auth import security_jwt
from services.bookmark import BookmarkService, get_bookmark_service

router = APIRouter()


@router.get(
    path='/',
    status_code=http_status.HTTP_200_OK,
    response_model=GetBookmarksListResponse
)
async def get_bookmarks(
        user: Annotated[dict, Depends(security_jwt(required_roles=['user']))],
        skip: int = 0,
        limit: int = 10,
        user_id: UUID = None,
        movie_id: UUID = None,
        bookmark_service: BookmarkService = Depends(get_bookmark_service)
) -> GetBookmarksListResponse:
    """Get bookmarks list."""
    bookmarks, count = await bookmark_service.get_bookmarks_list(
        skip=skip,
        limit=limit,
        user_id=user_id,
        movie_id=movie_id
    )
    return GetBookmarksListResponse(**{"data": bookmarks, "meta": {"count": count}})


@router.get(
    path='/{bookmark_id}',
    status_code=http_status.HTTP_200_OK,
    response_model=Bookmark
)
async def get_bookmark(
        user: Annotated[dict, Depends(security_jwt(required_roles=['user']))],
        bookmark_id: UUID,
        bookmark_service: BookmarkService = Depends(get_bookmark_service)
) -> Bookmark:
    """Get bookmark."""
    bookmark = await bookmark_service.get_bookmark(bookmark_id=bookmark_id)
    return bookmark


@router.post(
    path='/',
    status_code=http_status.HTTP_201_CREATED,
    response_model=Bookmark
)
async def create_bookmark(
        user: Annotated[dict, Depends(security_jwt(required_roles=['user']))],
        create_param: CreateBookmarkRequest,
        bookmark_service: BookmarkService = Depends(get_bookmark_service)
) -> Bookmark:
    """Create bookmark."""
    exists, _ = await bookmark_service.get_bookmarks_list(
        user_id=create_param.user_id,
        movie_id=create_param.movie_id
    )
    if exists:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="Already exists.")
    bookmark = await bookmark_service.create_bookmark(**create_param.model_dump())
    return bookmark

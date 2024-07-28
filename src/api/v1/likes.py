from uuid import UUID

from starlette import status as http_status
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.likes import Like, CreateLikeRequest, GetLikesListResponse
from services.auth import security_jwt
from services.like import LikeService, get_like_service

router = APIRouter()


@router.get(
    path='/',
    status_code=http_status.HTTP_200_OK,
    response_model=GetLikesListResponse
)
async def get_likes(
        user: Annotated[dict, Depends(security_jwt(required_roles=['user']))],
        skip: int = 0,
        limit: int = 10,
        user_id: UUID = None,
        movie_id: UUID = None,
        like_service: LikeService = Depends(get_like_service)
) -> GetLikesListResponse:
    """Get likes list."""
    likes, count = await like_service.get_likes_list(
        skip=skip,
        limit=limit,
        user_id=user_id,
        movie_id=movie_id
    )
    return GetLikesListResponse(**{"data": likes, "meta": {"count": count}})


@router.get(
    path='/{like_id}',
    status_code=http_status.HTTP_200_OK,
    response_model=Like
)
async def get_like(
        user: Annotated[dict, Depends(security_jwt(required_roles=['user']))],
        like_id: UUID,
        like_service: LikeService = Depends(get_like_service)
) -> Like:
    """Get like."""
    like = await like_service.get_like(like_id=like_id)
    return like


@router.post(
    path='/',
    status_code=http_status.HTTP_201_CREATED,
    response_model=Like
)
async def create_like(
        user: Annotated[dict, Depends(security_jwt(required_roles=['user']))],
        create_param: CreateLikeRequest,
        like_service: LikeService = Depends(get_like_service)
) -> Like:
    """Create like."""
    exists, _ = await like_service.get_likes_list(
        user_id=create_param.user_id,
        movie_id=create_param.movie_id
    )
    if exists:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="Already exists.")
    like = await like_service.create_like(**create_param.model_dump())
    return like

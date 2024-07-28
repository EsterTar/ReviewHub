from uuid import UUID

from starlette import status as http_status
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas.reviews import Review, CreateReviewRequest, GetReviewsListResponse
from services.auth import security_jwt
from services.review import ReviewService, get_review_service

router = APIRouter()


@router.get(
    path='/',
    status_code=http_status.HTTP_200_OK,
    response_model=GetReviewsListResponse
)
async def get_reviews(
        user: Annotated[dict, Depends(security_jwt(required_roles=['user']))],
        skip: int = 0,
        limit: int = 10,
        user_id: UUID = None,
        movie_id: UUID = None,
        review_service: ReviewService = Depends(get_review_service)
) -> GetReviewsListResponse:
    """Get reviews list."""
    reviews, count = await review_service.get_reviews_list(
        skip=skip,
        limit=limit,
        user_id=user_id,
        movie_id=movie_id
    )
    return GetReviewsListResponse(**{"data": reviews, "meta": {"count": count}})


@router.get(
    path='/{review_id}',
    status_code=http_status.HTTP_200_OK,
    response_model=Review
)
async def get_review(
        user: Annotated[dict, Depends(security_jwt(required_roles=['user']))],
        review_id: UUID,
        review_service: ReviewService = Depends(get_review_service)
) -> Review:
    """Get review."""
    review = await review_service.get_review(review_id=review_id)
    return review


@router.post(
    path='/',
    status_code=http_status.HTTP_201_CREATED,
    response_model=Review
)
async def create_review(
        user: Annotated[dict, Depends(security_jwt(required_roles=['user']))],
        create_param: CreateReviewRequest,
        review_service: ReviewService = Depends(get_review_service)
) -> Review:
    """Create review."""
    exists, _ = await review_service.get_reviews_list(
        user_id=create_param.user_id,
        movie_id=create_param.movie_id
    )
    if exists:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="Already exists.")
    review = await review_service.create_review(**create_param.model_dump())
    return review

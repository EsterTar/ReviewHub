import uuid

from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status as http_status
import pytest
from functional.schemas.bookmarks import Bookmark
from functional.utils.common import replace_dynamic_attrs


@pytest.mark.parametrize(
    'method, api_url, payload, expected_answer, test_name',
    [
        (
                'GET',
                '/',
                {},
                {
                    'status': http_status.HTTP_200_OK,
                    'body': {
                        'data': [
                            {
                                '_id': '...',
                                'user_id': '...',
                                'movie_id': '...',
                                'created_at': '...'
                            }
                        ],
                        'meta': {'count': 1}}
                },
                'get_bookmarks_list-one_exists'
        ),
        (
                'GET',
                '/...',
                {},
                {
                    'status': http_status.HTTP_200_OK,
                    'body': {
                        '_id': '...',
                        'user_id': '...',
                        'movie_id': '...',
                        'created_at': '...'
                    }
                },
                'get_bookmark-exists'
        ),
        (
                'POST',
                '/',
                {
                    'user_id': '...',
                    'movie_id': '...',
                },
                {
                    'status': http_status.HTTP_201_CREATED,
                    'body': {
                        '_id': '...',
                        'user_id': '...',
                        'movie_id': '...',
                        'created_at': '...'
                    }
                },
                'create_bookmark-success'
        )
    ]
)
@pytest.mark.asyncio(scope="session")
async def test_bookmarks(
        make_request,
        mongodb_client: AsyncIOMotorClient,
        method: str,
        api_url: str,
        payload: dict,
        expected_answer: dict,
        test_name: str
):
    await Bookmark.delete_all()
    api_url_prefix = '/api/v1/bookmarks'
    if test_name == "default":
        response = await make_request(
            method=method,
            api_url=f'{api_url_prefix}{api_url}',
            payload=payload
        )
    elif test_name == 'get_bookmarks_list-one_exists':
        await Bookmark.delete_all()
        bookmark = Bookmark(
            user_id=uuid.uuid4(),
            movie_id=uuid.uuid4(),
        )
        await bookmark.insert()
        response = await make_request(
            method=method,
            api_url=f'{api_url_prefix}{api_url}',
            payload=payload
        )
        expected_answer["body"]["data"][0] = replace_dynamic_attrs(
            expected_answer["body"]["data"][0],
            response["body"]["data"][0]
        )
    elif test_name == 'get_bookmark-exists':
        await Bookmark.delete_all()
        bookmark = Bookmark(
            user_id=uuid.uuid4(),
            movie_id=uuid.uuid4(),
        )
        await bookmark.insert()
        api_url = api_url.replace("...", str(bookmark.id))
        response = await make_request(
            method=method,
            api_url=f'{api_url_prefix}{api_url}',
            payload=payload
        )
        expected_answer["body"] = replace_dynamic_attrs(
            expected_answer["body"],
            response["body"]
        )
    elif test_name == 'create_bookmark-success':
        user_id = uuid.uuid4()
        movie_id = uuid.uuid4()
        payload["user_id"] = str(user_id)
        payload["movie_id"] = str(movie_id)
        response = await make_request(
            method=method,
            api_url=f'{api_url_prefix}{api_url}',
            payload=payload
        )
        expected_answer["body"] = replace_dynamic_attrs(
            expected_answer["body"],
            response["body"]
        )
    else:
        raise ValueError(f"Unknown test_name: {test_name}")

    if expected_answer['body']:
        print('expected:', expected_answer['body'])
        print('response:', response['body'])
        assert response['body'] == expected_answer['body']
    assert response['status'] == expected_answer['status']

import aiohttp
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from functional import config
from functional.clients.mongo_db import MongoClient

settings = config.get_settings()


@pytest_asyncio.fixture(name='cl_session', scope='session')
async def cl_session():
    cl_session = aiohttp.ClientSession()
    yield cl_session
    await cl_session.close()


@pytest_asyncio.fixture(name='make_request', scope='session')
async def make_request(cl_session):
    async def inner(method, api_url, payload=None, headers=None):
        full_url = f'http://{settings.app_host}:{settings.app_port}' + api_url
        async with cl_session.request(
            method=method,
            url=full_url,
            headers=headers,
            json=payload
        ) as response:
            status = response.status
            body = await response.json()
            return {'status': status, 'body': body}
    return inner


@pytest_asyncio.fixture(name='mongodb_client', scope='session')
async def mongodb_client(cl_session) -> AsyncIOMotorClient:
    client = MongoClient()
    session = await client.get()
    return session

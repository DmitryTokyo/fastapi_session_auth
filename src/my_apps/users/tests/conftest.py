import pytest_asyncio
from sqlalchemy import text

from src.my_apps.conftest import test_session

from src.my_apps.users.tests.factories import UserFactory


@pytest_asyncio.fixture
async def clean_users(test_session):
    await test_session.execute(text('DELETE FROM app_user'))
    await test_session.commit()


@pytest_asyncio.fixture
async def user_factory():
    async def _create_user(username: str = 'test username', hashed_password: str = 'hashed_password') -> UserFactory:
        return await UserFactory(username=username, hashed_password=hashed_password)
    return _create_user



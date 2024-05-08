from asyncio import current_task
import logging
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session
from starlette.testclient import TestClient

from src.config.base import settings
from src.db.db_init import Base
from src.server import app

logger = logging.getLogger(__name__)

test_engine = create_async_engine(settings.TEST_DB_URL, echo=False)
AsyncSessionFactory = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
async_sc_session = async_scoped_session(AsyncSessionFactory, scopefunc=current_task)


@pytest_asyncio.fixture
async def test_db_engine():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    yield test_engine
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def test_session(test_db_engine) -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest.fixture(scope='module')
def test_server_url() -> str:
    return 'http://fast-api-test-server'


@pytest.fixture(scope='module')
def client(test_server_url: str) -> Generator:
    yield TestClient(app, base_url=test_server_url, follow_redirects=False)

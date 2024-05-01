import asyncio
from asyncio import current_task
import logging
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from pytest_asyncio import is_async_test
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session

from src.config.base import settings
from src.db.db_init import Base

logger = logging.getLogger(__name__)

engine_test = create_async_engine(settings.TEST_DB_URL, echo=False)
AsyncSessionFactory = async_sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
async_sc_session = async_scoped_session(AsyncSessionFactory, scopefunc=current_task)


@pytest_asyncio.fixture(scope='module')
async def prepare_database(event_loop) -> AsyncGenerator:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='module')
async def test_session(prepare_database, event_loop) -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest.fixture(scope='module', autouse=True)
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

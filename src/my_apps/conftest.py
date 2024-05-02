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

test_engine = create_async_engine("sqlite+aiosqlite:///my_temp_db.db", echo=False)
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
        await conn.run_sync(Base.metadata.drop_all)
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


from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory

from src.my_apps.conftest import async_sc_session


class BaseFactory(AsyncSQLAlchemyFactory):
    """Base class for all factories."""

    class Meta:
        abstract = True
        sqlalchemy_session = async_sc_session
        sqlalchemy_session_persistence = 'commit'

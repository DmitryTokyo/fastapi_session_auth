import os
import secrets
from pathlib import Path
from typing import ClassVar

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Base(BaseSettings):
    DEV: bool = os.environ.get('DEV', default=False) is True
    PROJECT_NAME: str = 'Grab my bills'
    BACKEND_DIR: ClassVar = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ROOT_DIR: ClassVar = os.path.dirname(BACKEND_DIR)
    OPENAPI_URL: str = '/openapi_schema.json'
    SECRET_KEY: str = os.environ.get('SECRET_KEY', default=secrets.token_urlsafe(32))
    HASH_ALGORITHM: str = 'HS256'
    ADMIN_SESSION_EXPIRATION_SECONDS: int = 60 * 60 * 24

    DB_URL: str = os.getenv('DB_URL', default='sqlite:///sqlite3.db')
    TEST_DB_URL: str = os.getenv('TEST_DB_URL', default='sqlite+aiosqlite:///test_db.db')
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = [
        'http://localhost',
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'http://127.0.0.1',
    ]
    TEMPLATES_ROOT: Path = Path('src/my_apps') / 'templates'
    MEDIA_ROOT: str = f'{BACKEND_DIR}/media/'


settings = Base()

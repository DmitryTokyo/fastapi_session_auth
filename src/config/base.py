import os
from pathlib import Path
from typing import ClassVar

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    dev: bool = False
    project_name: str = 'Grab my bills'
    backend_dir: ClassVar = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root_dir: ClassVar = os.path.dirname(backend_dir)
    openapi_url: str = '/openapi_schema.json'
    secret_key: str = 'secret_key'
    hash_algorithm: str = 'HS256'
    admin_session_expiration_seconds: int = 60 * 60 * 24

    db_url: str = 'sqlite+aiosqlite:///sqlite3.db'
    test_db_url: str = 'sqlite+aiosqlite:///test_db.db'
    backend_cors_origins: list[AnyHttpUrl] = [
        'http://localhost',
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'http://127.0.0.1',
    ]
    templates_root: Path = Path('src/my_apps') / 'templates'
    media_root: str = f'{backend_dir}/media/'


settings = Settings()

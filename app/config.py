# flake8: noqa

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import final, Literal

LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',  # first search .dev.env, then .prod.env
        env_file_encoding='utf-8',
        case_sensitive=False,
    )

    run_type: str = 'prod'
    debug: bool = True

    log_level: Literal[
        'debug',
        'info',
        'warning',
        'error',
        'critical',
    ] = 'info'

    log_format: str = LOG_DEFAULT_FORMAT

    server_host: str = 'localhost'
    domain: str = 'localhost'

    # auth config
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1
    SECRET_KEY: str = 'secret'
    ALGORITHM: str = 'HS256'

    # uvicorn config
    host: str = '0.0.0.0'
    port: int = 8000
    reload: bool = True
    workers: int | None = None

    # cors
    cors_origins: list[str] = ['*']
    cors_credentials: bool = True
    cors_methods: list[str] = ['*']
    cors_headers: list[str] = ['*']

    # database config
    async_db_url: str = 'postgresql+asyncpg://db_user:db_pass@db_host:db_port/db_name'
    sync_db_url: str = 'postgresql+psycopg2://db_user:db_pass@db_host:db_port/db_name'

    db_echo: bool = False
    db_echo_pool: bool = False
    db_pool_size: int = 5
    db_pool_pre_ping: bool = True
    db_max_overflow: int = 10

    redis_url: str = f'redis://{server_host}:6379/1'


@lru_cache()  # get it from memory
def get_config() -> Settings:
    return Settings()

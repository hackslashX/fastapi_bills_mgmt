import logging

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine


class DatabaseConfig(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_DATABASE: str
    CONN_STRING: str = (
        "postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
    )


class JWTConfig(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int


class Environment(BaseSettings):
    APP_ENVIRONMENT: str
    DB_BIND: str = "master"


class Configuration:
    ENVIRONMENT: Environment = Environment()
    APP_ENVIRONMENT: str = ENVIRONMENT.APP_ENVIRONMENT
    DB_BIND: str = ENVIRONMENT.DB_BIND

    # DB Configuration
    DB_CONFIG: DatabaseConfig = DatabaseConfig()

    # SQLAlchemy Engines
    SQLALCHEMY_ENGINES: dict = {
        DB_BIND: create_async_engine(
            DB_CONFIG.CONN_STRING.format(
                username=DB_CONFIG.DB_USERNAME,
                password=DB_CONFIG.DB_PASSWORD,
                host=DB_CONFIG.DB_HOST,
                port=DB_CONFIG.DB_PORT,
                database=DB_CONFIG.DB_DATABASE,
            ),
            echo=False,
        ),
    }

    # Alembic URLs
    # Alembic requires sync engines instead of async ones
    ALEMBIC_URLS: dict = {
        DB_BIND: "postgresql+psycopg://{username}:{password}@{host}:{port}/{database}".format(
            username=DB_CONFIG.DB_USERNAME,
            password=DB_CONFIG.DB_PASSWORD,
            host=DB_CONFIG.DB_HOST,
            port=DB_CONFIG.DB_PORT,
            database=DB_CONFIG.DB_DATABASE,
        ),
    }

    # JWT Configuration
    JWT_CONFIG: JWTConfig = JWTConfig()

    # Logging
    LOGS_DIR: str = ".logs"
    LOGGING_LEVEL: int = logging.WARNING

    # API
    API_PREFIX: str = "api"


config = Configuration()

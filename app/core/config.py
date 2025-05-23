from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Personal Finance Tracker"
    DATABASE_URL_MASTER: str
    DATABASE_URL_REPLICA: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REDIS_URL: str
    STATS_SERVICE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()

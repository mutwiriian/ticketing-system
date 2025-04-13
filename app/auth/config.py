from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET: str
    ALGORITHM: str
    TOKEN_EXPIRY: int
    DB_URL: str
    TEMP_DB_URL: str

    model_config = SettingsConfigDict(env_file="../.env", case_sensitive=True)

@lru_cache
def get_settings():
    return Settings()
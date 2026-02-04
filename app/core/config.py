from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Task Manager API"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()

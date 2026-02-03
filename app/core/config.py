from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Task Manager API"


settings = Settings()

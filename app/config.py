from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings. Each one can be overridden by an environment variable or a .env file,
    for example SECRET_KEY=... or DATABASE_URL=..."""

    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Expense Tracker API"
    database_url: str = "sqlite:///./expenses.db"
    secret_key: str = "dev-only-secret-key-change-me-in-production"
    access_token_minutes: int = 30
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()

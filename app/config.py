from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")
    redis_url: str = Field(..., env="REDIS_URL")

    # Email settings
    smtp_server: str = Field("smtp.gmail.com", env="SMTP_SERVER")
    smtp_port: int = Field(587, env="SMTP_PORT")
    smtp_username: str = Field(..., env="SMTP_USERNAME")
    smtp_password: str = Field(..., env="SMTP_PASSWORD")
    sender_email: str = Field(..., env="SENDER_EMAIL")
    verification_base_url: str = Field("http://localhost:8000/verify", env="VERIFICATION_BASE_URL")

    user_delete_timeout: int = Field(..., env="USER_DELETE_TIMEOUT")
    log_destinations: str = Field(..., env="LOG_DESTINATIONS")
    log_file_path: str = Field(..., env="LOG_FILE_PATH")

    model_config = SettingsConfigDict(env_file=".env.backend", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

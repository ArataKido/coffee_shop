from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

env = ".env.backend"

class PostgresConfig(BaseSettings):
    host:     str = Field(..., env="POSTGRES_HOST", alias="POSTGRES_HOST")
    port:     int = Field(..., env="POSTGRES_PORT", alias="POSTGRES_PORT")
    user:    str = Field(..., env="POSTGRES_USER", alias="POSTGRES_USER")
    password: str = Field(..., env="POSTGRES_PASSWORD", alias="POSTGRES_PASSWORD")
    database: str = Field(..., env="POSTGRES_DB", alias="POSTGRES_DB")

    model_config = SettingsConfigDict(env_file=env, env_file_encoding="utf-8", extra="ignore")

class RedisConfig(BaseSettings):
    redis_url: str = Field(..., env="REDIS_URL")

    model_config = SettingsConfigDict(env_file=env, env_file_encoding="utf-8", extra="ignore")

class SmtpConfig(BaseSettings):
    smtp_server:    str = Field("smtp.gmail.com", env="SMTP_SERVER")
    smtp_port:      int = Field(587, env="SMTP_PORT")
    smtp_username:  str = Field(..., env="SMTP_USERNAME")
    smtp_password:  str = Field(..., env="SMTP_PASSWORD")
    sender_email:   str = Field(..., env="SENDER_EMAIL")

    model_config = SettingsConfigDict(env_file=env, env_file_encoding="utf-8", extra="ignore")

class AppConfig(BaseSettings):
    user_delete_timeout:         int = Field(..., env="USER_DELETE_TIMEOUT")
    log_destinations:            str = Field(..., env="LOG_DESTINATIONS")
    log_file_path:               str = Field(..., env="LOG_FILE_PATH")

    secret_key:                  str = Field(..., env="SECRET_KEY")
    algorithm:                   str = Field(..., env="ALGORITHM")
    verification_base_url:       str = Field("http://localhost:8000/verify", env="VERIFICATION_BASE_URL")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")

    model_config = SettingsConfigDict(env_file=env, env_file_encoding="utf-8", extra="ignore")

class Config(BaseSettings):
    postgres:   PostgresConfig = Field(default_factory=lambda: PostgresConfig())
    redis:      RedisConfig    = Field(default_factory=lambda: RedisConfig())
    smtp:       SmtpConfig     = Field(default_factory=lambda: SmtpConfig())
    app:        AppConfig      = Field(default_factory=lambda: AppConfig())

    model_config = SettingsConfigDict(env_file=env, env_file_encoding="utf-8", extra="ignore")

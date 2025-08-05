from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Using an env file to load environment variables
    # rather than hardcoding them
    class Config:
        env_file = ".env"


settings = Settings()
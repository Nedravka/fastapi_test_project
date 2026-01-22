from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str
    API_KEY_NAME: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    debug: bool
    project_name: str = "Organization API"
    version: str = "1.0.0"

    @property
    def db_url(self):
        return (f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@"
                f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

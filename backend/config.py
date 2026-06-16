import os


class Settings:
    """
    Настройки приложения.
    Значения берутся из переменных окружения (docker-compose),
    при их отсутствии используются дефолты.
    """

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    DATABASE_URL: str
    APP_HOST: str
    APP_PORT: int
    SECRET_KEY: str
    TESTING: bool

    def __init__(self) -> None:
        self.TESTING = os.getenv("TESTING", "0") == "1"

        self.POSTGRES_USER = os.getenv("POSTGRES_USER", "twitter_user")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "twitter_password")
        self.POSTGRES_DB = os.getenv("POSTGRES_DB", "twit_db")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
        self.POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

        if self.TESTING:
            self.DATABASE_URL = os.getenv("DATABASE_URL",
                                          "sqlite:///./test.db")

        else:
            self.DATABASE_URL = os.getenv(
                "DATABASE_URL",
                f"postgresql://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}",
            )

        self.APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
        self.APP_PORT = int(os.getenv("APP_PORT", "8080"))
        self.SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL


settings = Settings()

from pydantic import model_validator
from pydantic_settings import BaseSettings

from domain.entities.bet import BetState


class GeneralSettings(BaseSettings):
    base_bet_state: BetState = BetState.NEW


class KafkaSettings(BaseSettings):
    kafka_url: str
    event_change_topic: str = 'event_change_topic'
    new_event_topic: str = "new_event_topic"
    new_bet_topic: str = "new_bet_topic"


class PostgresSettings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB_URL: str | None = None

    @model_validator(mode="before")  # noqa
    @classmethod
    def assemble_postgres_url(cls, values: dict[str, str]) -> dict[str, str]:
        if values.get("POSTGRES_DB_URL"):
            return values

        username = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        host = values.get("POSTGRES_HOST")
        port = values.get("POSTGRES_PORT")
        db_name = values.get("POSTGRES_DB")
        values["POSTGRES_DB_URL"] = (
            f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}"
        )

        return values

    @property
    def test_postgres_db(self) -> str:
        return f"test_{self.POSTGRES_DB}"

    @property
    def test_postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.test_postgres_db}" # noqa


class Settings(PostgresSettings, GeneralSettings, KafkaSettings):
    ...


settings = Settings()

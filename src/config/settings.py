from typing import Literal

from pydantic import ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.exceptions.etl import ConfigurationError


class Settings(BaseSettings):
    app_env: str = "development"

    api_url: str

    latitude: float
    longitude: float

    output_path: str = "data/raw"
    processed_path: str = "data/processed"

    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value: float) -> float:
        if not -90 <= value <= 90:
            raise ValueError(
                "Latitude must be between -90 and 90"
            )

        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: float) -> float:
        if not -180 <= value <= 180:
            raise ValueError(
                "Longitude must be between -180 and 180"
            )

        return value


def get_settings() -> Settings:
    try:
        return Settings()
    
    except ValidationError as exc:
        raise ConfigurationError(
            "Application configuration is invalid"
        ) from exc
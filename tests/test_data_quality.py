import pandas as pd
import pytest

from src.exceptions.etl import DataQualityError
from src.quality.weather import WeatherDataQuality


def test_valid_weather_dataframe_passes():

    dataframe = pd.DataFrame(
        [
            {
                "latitude": -12.0464,
                "longitude": -77.0428,
                "timezone": "America/Lima",
                "timestamp": "2026-07-27T12:00",
                "temperature_c": 18.5,
                "humidity_pct": 80,
                "wind_speed_kmh": 12.3,
            }
        ]
    )

    validator = WeatherDataQuality()
    result = validator.validate(dataframe)

    assert not result.empty


def test_invalid_humidity_fails():

    dataframe = pd.DataFrame(
        [
            {
                "latitude": -12.0464,
                "longitude": -77.0428,
                "timezone": "America/Lima",
                "timestamp": "2026-07-27T12:00",
                "temperature_c": 18.5,
                "humidity_pct": 150,
                "wind_speed_kmh": 12.3,
            }
        ]
    )

    validator = WeatherDataQuality()

    with pytest.raises(DataQualityError):
        validator.validate(dataframe)


def test_negative_wind_speed_fails():

    dataframe = pd.DataFrame(
        [
            {
                "latitude": -12.0464,
                "longitude": -77.0428,
                "timezone": "America/Lima",
                "timestamp": "2026-07-27T12:00",
                "temperature_c": 18.5,
                "humidity_pct": 80,
                "wind_speed_kmh": -10,
            }
        ]
    )

    validator = WeatherDataQuality()

    with pytest.raises(DataQualityError):
        validator.validate(dataframe)
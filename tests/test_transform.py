import pandas as pd

from src.transform.weather import WeatherTransformer


def test_weather_transformer_returns_dataframe():
    raw_data = {
        "latitude": -12.0464,
        "longitude": -77.0428,
        "timezone": "America/Lima",
        "current": {
            "time": "2026-07-27T12:00",
            "temperature_2m": 18.5,
            "relative_humidity_2m": 80,
            "wind_speed_10m": 12.3,
        },
    }

    transformer = WeatherTransformer()
    dataframe = transformer.transform(raw_data)

    assert isinstance(
        dataframe,
        pd.DataFrame,
    )

    assert len(dataframe) == 1
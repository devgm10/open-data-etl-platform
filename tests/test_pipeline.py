import pandas as pd

from src.extract.weather_api import WeatherAPIExtractor
from src.main import run_pipeline
from src.quality.weather import WeatherDataQuality
from src.storage.local_storage import LocalStorage
from src.storage.processed_storage import ProcessedStorage
from src.transform.weather import WeatherTransformer


def test_weather_etl_pipeline(tmp_path, monkeypatch):

    weather_data = {
        "latitude": -12.0464,
        "longitude": -77.0428,
        "timezone": "America/Lima",
        "current": {
            "time": "2026-07-28T00:00",
            "temperature_2m": 20.5,
            "relative_humidity_2m": 80,
            "wind_speed_10m": 10.2,
        },
    }

    def mock_extract(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        return weather_data

    monkeypatch.setattr(
        WeatherAPIExtractor,
        "extract",
        mock_extract,
    )

    raw_path = tmp_path / "raw"
    processed_path = tmp_path / "processed"

    extractor = WeatherAPIExtractor(
        api_url="https://api.open-meteo.com/v1/forecast",
    )

    storage = LocalStorage(
        base_path=str(raw_path),
    )

    processed_storage = ProcessedStorage(
        base_path=str(processed_path),
    )

    transformer = WeatherTransformer()

    data_quality = WeatherDataQuality()

    run_pipeline(
        extractor=extractor,
        storage=storage,
        transformer=transformer,
        data_quality=data_quality,
        processed_storage=processed_storage,
        latitude=-12.0464,
        longitude=-77.0428,
    )

    raw_file = raw_path / "weather.json"
    processed_file = processed_path / "weather.csv"

    assert raw_file.exists()
    assert processed_file.exists()

    dataframe = pd.read_csv(processed_file)

    expected_columns = {
        "latitude",
        "longitude",
        "timezone",
        "timestamp",
        "temperature_c",
        "humidity_pct",
        "wind_speed_kmh",
    }

    assert set(dataframe.columns) == expected_columns

    assert dataframe.iloc[0]["latitude"] == -12.0464
    assert dataframe.iloc[0]["longitude"] == -77.0428
    assert dataframe.iloc[0]["temperature_c"] == 20.5
    assert dataframe.iloc[0]["humidity_pct"] == 80
    assert dataframe.iloc[0]["wind_speed_kmh"] == 10.2
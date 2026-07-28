import sys

from src.config.settings import get_settings
from src.exceptions.etl import ETLException
from src.extract.weather_api import WeatherAPIExtractor
from src.quality.weather import WeatherDataQuality
from src.storage.local_storage import LocalStorage
from src.storage.processed_storage import ProcessedStorage
from src.transform.weather import WeatherTransformer
from src.utils.logger import get_logger


def run_pipeline(
    extractor: WeatherAPIExtractor,
    storage: LocalStorage,
    transformer: WeatherTransformer,
    data_quality: WeatherDataQuality,
    processed_storage: ProcessedStorage,
    latitude: float,
    longitude: float,
) -> None:

    logger = get_logger(
        __name__,
    )

    logger.info(
        "Starting ETL extraction process"
    )

    weather_data = extractor.extract(
        latitude=latitude,
        longitude=longitude,
    )

    storage.save_json(
        data=weather_data,
        filename="weather.json",
    )

    raw_data = storage.load_json(
        filename="weather.json",
    )

    weather_dataframe = transformer.transform(
        raw_data,
    )

    validated_dataframe = data_quality.validate(
        weather_dataframe,
    )

    processed_storage.save_csv(
        dataframe=validated_dataframe,
        filename="weather.csv",
    )

    logger.info(
        "ETL extraction process completed successfully"
    )


def main() -> None:

    settings = get_settings()

    extractor = WeatherAPIExtractor(
        api_url=settings.api_url,
    )

    storage = LocalStorage(
        base_path=settings.output_path,
    )

    processed_storage = ProcessedStorage(
        base_path=settings.processed_path,
    )

    transformer = WeatherTransformer()

    data_quality = WeatherDataQuality()

    run_pipeline(
        extractor=extractor,
        storage=storage,
        transformer=transformer,
        data_quality=data_quality,
        processed_storage=processed_storage,
        latitude=settings.latitude,
        longitude=settings.longitude,
    )


if __name__ == "__main__":

    try:
        main()

    except ETLException as exc:

        logger = get_logger(
            __name__,
            "INFO",
        )

        logger.error(
            "%s",
            exc,
        )

        sys.exit(1)
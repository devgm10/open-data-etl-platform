import sys

from src.config.settings import get_settings
from src.exceptions.etl import ETLException
from src.extract.weather_api import WeatherAPIExtractor
from src.storage.local_storage import LocalStorage
from src.utils.logger import get_logger


def main() -> None:

    settings = get_settings()
    logger = get_logger(__name__, settings.log_level)

    logger.info(
        "Starting ETL extraction process"
    )

    extractor = WeatherAPIExtractor(
        api_url=settings.api_url,
    )

    storage = LocalStorage(
        base_path=settings.output_path,
    )

    weather_data = extractor.extract(
        latitude=settings.latitude,
        longitude=settings.longitude,
    )

    storage.save_json(
        data=weather_data,
        filename="weather.json",
    )

    logger.info(
        "ETL extraction process completed successfully"
    )


if __name__ == "__main__":
    try:
        main()

    except ETLException as exc:
        logger = get_logger(__name__, "INFO")
        logger.error("%s", exc)
        sys.exit(1)
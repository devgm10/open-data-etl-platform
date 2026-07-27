import httpx

from src.exceptions.etl import ExtractionError
from src.utils.logger import get_logger

logger = get_logger(__name__)

class WeatherAPIExtractor:
    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    def extract(self, latitude: float, longitude: float) -> dict:

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "wind_speed_10m"
            ),
        }

        logger.info(
            "Requesting weather data for coordinates: "
            "latitude=%s, longitude=%s",
            latitude,
            longitude,
        )

        logger.debug(
            "Weather API request parameters: %s",
            params,
        )

        try:
            response = httpx.get(
                self.api_url,
                params=params,
                timeout=10.0,
            )

            response.raise_for_status()

        except httpx.TimeoutException as exc:
            logger.error(
                "Weather API request timed out"
            )

            raise ExtractionError(
                "Weather API request timed out"
            ) from exc

        except httpx.HTTPStatusError as exc:
            logger.error(
                "Weather API returned HTTP error: status_code=%s",
                exc.response.status_code,
            )

            raise ExtractionError(
                "Weather API returned an HTTP error"
            ) from exc

        except httpx.RequestError as exc:
            logger.error(
                "Weather API request failed: %s",
                exc,
            )

            raise ExtractionError(
                "Weather API request failed"
            ) from exc

        logger.info(
            "Weather data extracted successfully"
        )

        return response.json()
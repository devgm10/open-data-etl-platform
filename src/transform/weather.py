import pandas as pd

from src.exceptions.etl import TransformationError
from src.utils.logger import get_logger

logger = get_logger(__name__)

class WeatherTransformer:

    def transform(self, data: dict) -> pd.DataFrame:
        logger.info(
            "Starting weather data transformation"
        )

        try:
            current = data["current"]
            dataframe = pd.DataFrame([
                {
                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                    "timezone": data["timezone"],
                    "timestamp": current["time"],
                    "temperature_c": current["temperature_2m"],
                    "humidity_pct": current[
                        "relative_humidity_2m"
                    ],
                    "wind_speed_kmh": current[
                        "wind_speed_10m"
                    ],
                }
            ])

        except KeyError as exc:
            logger.error(
                "Missing required field in weather data: %s",
                exc,
            )

            raise TransformationError(
                "Weather data is missing required fields"
            ) from exc

        logger.info(
            "Weather data transformation completed successfully"
        )

        logger.debug(
            "Transformed dataframe:\n%s",
            dataframe,
        )

        return dataframe
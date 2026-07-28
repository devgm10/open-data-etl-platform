from typing import ClassVar

import pandas as pd

from src.exceptions.etl import DataQualityError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class WeatherDataQuality:

    REQUIRED_COLUMNS: ClassVar[set[str]] = {
        "latitude",
        "longitude",
        "timezone",
        "timestamp",
        "temperature_c",
        "humidity_pct",
        "wind_speed_kmh",
    }

    def validate(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        logger.info(
            "Starting weather data quality validation"
        )

        self._validate_not_empty(dataframe)
        self._validate_columns(dataframe)
        self._validate_nulls(dataframe)
        self._validate_ranges(dataframe)
        self._validate_timestamp(dataframe)

        logger.info(
            "Weather data quality validation completed successfully"
        )

        return dataframe

    def _validate_not_empty(self, dataframe: pd.DataFrame) -> None:
        if dataframe.empty:
            raise DataQualityError(
                "Weather dataframe is empty"
            )

    def _validate_columns(self, dataframe: pd.DataFrame) -> None:
        actual_columns = set(dataframe.columns)
        missing_columns = (self.REQUIRED_COLUMNS - actual_columns)

        if missing_columns:
            raise DataQualityError(
                "Missing required columns: "
                f"{sorted(missing_columns)}"
            )

    def _validate_nulls(self, dataframe: pd.DataFrame) -> None:
        null_columns = (
            dataframe[list(self.REQUIRED_COLUMNS)].columns[
                dataframe[list(self.REQUIRED_COLUMNS)]
                .isnull()
                .any()
            ]
            .tolist()
        )

        if null_columns:
            raise DataQualityError(
                "Null values found in columns: "
                f"{sorted(null_columns)}"
            )

    def _validate_ranges(self, dataframe: pd.DataFrame) -> None:

        if not dataframe["latitude"].between(-90, 90).all():
            raise DataQualityError(
                "Latitude values are outside valid range"
            )

        if not dataframe["longitude"].between(-180, 180).all():
            raise DataQualityError(
                "Longitude values are outside valid range"
            )

        if not dataframe["temperature_c"].between(-100, 100).all():
            raise DataQualityError(
                "Temperature values are outside valid range"
            )

        if not dataframe["humidity_pct"].between(0, 100).all():
            raise DataQualityError(
                "Humidity values are outside valid range"
            )

        if (dataframe["wind_speed_kmh"] < 0).any():
            raise DataQualityError(
                "Wind speed cannot be negative"
            )

    def _validate_timestamp(self, dataframe: pd.DataFrame) -> None:
        try:
            pd.to_datetime(
                dataframe["timestamp"],
                errors="raise",
            )

        except (TypeError, ValueError) as exc:
            raise DataQualityError(
                "Invalid timestamp values"
            ) from exc
import pandas as pd
from pathlib import Path

from src.exceptions.etl import StorageError
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ProcessedStorage:
    def __init__(self, base_path: str) -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_csv(self, dataframe: pd.DataFrame, filename: str) -> Path:
        file_path = self.base_path / filename
        logger.info(
            "Saving processed data to: %s",
            file_path,
        )

        try:
            dataframe.to_csv(file_path, index=False)

        except OSError as exc:
            logger.error(
                "Failed to saved processed data: %s",
                exc,
            )

            raise StorageError(
                f"Failed to save processed data to {file_path}"
            ) from exc

        logger.info(
            "Processed data saved successfully: %s",
            file_path,
        )

        return file_path
import json
from pathlib import Path

from src.exceptions.etl import StorageError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LocalStorage:
    def __init__(self, base_path: str) -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_json(self, data: dict, filename: str) -> Path:
        file_path = self.base_path / filename
        logger.info(
            "Saving raw data to: %s",
            file_path,
        )

        try:
            with file_path.open(
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4,
                )

        except OSError as exc:

            logger.error(
                "Failed to save raw data: %s",
                exc,
            )

            raise StorageError(
                f"Failed to save data to {file_path}"
            ) from exc

        logger.info(
            "Raw data saved successfully: %s",
            file_path,
        )

        return file_path
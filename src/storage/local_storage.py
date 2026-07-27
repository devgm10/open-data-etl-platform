import json
from pathlib import Path

class LocalStorage:
    def __init__(self, base_path: str = "data/raw") -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_json(self, data: dict, filename: str) -> Path:
        file_path = self.base_path / filename

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

            return file_path
        
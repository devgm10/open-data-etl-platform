from src.extract.weather_api import WeatherAPIExtractor
from src.storage.local_storage import LocalStorage

def main() -> None:
    extractor = WeatherAPIExtractor()
    storage = LocalStorage()

    weather_data = extractor.extract(
        latitude=-12.0464,
        longitude=-77.0428
    )

    file_path = storage.save_json(
        data=weather_data,
        filename="weather.json",
    )

    print(f"Raw data saved successfully: {file_path}")
    
if __name__ == "__main__":
    main()
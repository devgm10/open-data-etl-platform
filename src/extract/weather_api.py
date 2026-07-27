import httpx


class WeatherAPIExtractor:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

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

        response = httpx.get(
            self.BASE_URL,
            params=params,
            timeout=10.0,
        )

        response.raise_for_status()

        return response.json()
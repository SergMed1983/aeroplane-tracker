from abc import ABC, abstractmethod
import requests

class AbstractAPI(ABC):
    """Базовый класс для работы с API."""

    @abstractmethod
    def connect(self) -> None:
        """Проверка доступности API."""

    @abstractmethod
    def get_data(self, country: str) -> list | dict:
        """Получение данных по стране."""


class NominatimAPI(AbstractAPI):
    BASE_URL = "https://nominatim.openstreetmap.org/search"

    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout
        self.headers = {"User-Agent": "aeroplane-tracker/1.0"}

    def connect(self) -> None:
        try:
            r = requests.get(self.BASE_URL, params={"q": "Spain", "format": "json"},
                             headers=self.headers, timeout=self.timeout)
            r.raise_for_status()
        except requests.RequestException as e:
            raise ConnectionError(f"Nominatim недоступен: {e}") from e

    def get_data(self, country: str) -> list:
        params = {"q": country, "format": "json", "limit": 1}
        try:
            r = requests.get(self.BASE_URL, params=params,
                             headers=self.headers, timeout=self.timeout)
            r.raise_for_status()
            data = r.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка запроса к Nominatim: {e}") from e
        except ValueError as e:
            raise ValueError(f"Некорректный JSON от Nominatim: {e}") from e
        return data if isinstance(data, list) else []

    def get_country_boundingbox(self, country: str) -> list[str] | None:
        data = self.get_data(country)
        if not data:
            return None
        return data[0].get("boundingbox")


class OpenSkyAPI(AbstractAPI):
    BASE_URL = "https://opensky-network.org/api/states/all"

    def __init__(self, timeout: int = 15) -> None:
        self.timeout = timeout
        self.nominatim = NominatimAPI(timeout=timeout)

    def connect(self) -> None:
        try:
            r = requests.get(self.BASE_URL, timeout=self.timeout)
            r.raise_for_status()
        except requests.RequestException as e:
            raise ConnectionError(f"OpenSky недоступен: {e}") from e

    def get_data(self, country: str) -> list:
        bbox = self.nominatim.get_country_boundingbox(country)
        if not bbox or len(bbox) != 4:
            return []
        # boundingbox: [south, north, west, east]
        south, north, west, east = map(float, bbox)
        params = {"lamin": south, "lamax": north,
                  "lomin": west, "lomax": east}
        try:
            r = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
            r.raise_for_status()
            data = r.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка запроса к OpenSky: {e}") from e
        except ValueError as e:
            raise ValueError(f"Некорректный JSON от OpenSky: {e}") from e
        return data.get("states") or []

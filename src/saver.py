import json
import os
from abc import ABC, abstractmethod

from src.aeroplane import Aeroplane


class AbstractSaver(ABC):
    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None: ...
    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None: ...
    @abstractmethod
    def get_aeroplanes(self, criteria: dict | None = None) -> list[dict]: ...


class JSONSaver(AbstractSaver):
    def __init__(self, filename: str = "data/aeroplanes.json") -> None:
        self.filename = filename
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read(self) -> list[dict]:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except FileNotFoundError, json.JSONDecodeError:
            return []

    def _write(self, data: list[dict]) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._read()
        data.append(aeroplane.to_dict())
        self._write(data)

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = [d for d in self._read() if d.get("callsign") != aeroplane.callsign]
        self._write(data)

    def get_aeroplanes(self, criteria: dict | None = None) -> list[dict]:
        data = self._read()
        if not criteria:
            return data
        result = data
        for key, value in criteria.items():
            result = [d for d in result if d.get(key) == value]
        return result

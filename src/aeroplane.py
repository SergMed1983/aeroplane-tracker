from __future__ import annotations


class Aeroplane:
    """Модель самолёта. Инкапсулирует данные и сравнение."""

    def __init__(
        self, callsign: str, origin_country: str, velocity: float, altitude: float
    ) -> None:
        if not isinstance(callsign, str) or not callsign.strip():
            raise ValueError("callsign должен быть непустой строкой")
        if not isinstance(origin_country, str) or not origin_country.strip():
            raise ValueError("origin_country должен быть непустой строкой")
        if not isinstance(velocity, (int, float)) or velocity < 0:
            raise ValueError("velocity должен быть числом >= 0")
        if not isinstance(altitude, (int, float)) or altitude < 0:
            raise ValueError("altitude должен быть числом >= 0")

        self.callsign = callsign.strip()
        self.origin_country = origin_country.strip()
        self.velocity = float(velocity)
        self.altitude = float(altitude)

    @classmethod
    def cast_to_object_list(cls, raw: list[list]) -> list["Aeroplane"]:
        """Превращает сырой ответ OpenSky (states) в список объектов."""
        result: list[Aeroplane] = []
        if not raw:
            return result
        for item in raw:
            try:
                # индексы OpenSky: 1 callsign, 2 origin_country, 7 altitude, 9 velocity
                callsign = item[1] or "UNKNOWN"
                country = item[2] or "UNKNOWN"
                altitude = item[7] if item[7] is not None else 0.0
                velocity = item[9] if item[9] is not None else 0.0
                result.append(cls(callsign, country, velocity, altitude))
            except (IndexError, TypeError, ValueError):
                continue  # битую строку пропускаем
        return result

    # сравнение по скорости (основное)
    def __lt__(self, other: "Aeroplane") -> bool:
        return self.velocity < other.velocity

    def __gt__(self, other: "Aeroplane") -> bool:
        return self.velocity > other.velocity

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.callsign == other.callsign

    # сравнение по высоте — отдельными методами
    def is_higher_than(self, other: "Aeroplane") -> bool:
        return self.altitude > other.altitude

    def is_faster_than(self, other: "Aeroplane") -> bool:
        return self.velocity > other.velocity

    def to_dict(self) -> dict:
        return {
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "altitude": self.altitude,
        }

    def __repr__(self) -> str:
        return (
            f"Aeroplane(callsign={self.callsign!r}, "
            f"country={self.origin_country!r}, "
            f"velocity={self.velocity}, altitude={self.altitude})"
        )

from src.aeroplane import Aeroplane
from src.api import OpenSkyAPI
from src.saver import JSONSaver


def filter_by_country(aeroplanes: list[Aeroplane], words: list[str]) -> list[Aeroplane]:
    if not words:
        return aeroplanes
    return [
        a
        for a in aeroplanes
        if any(w.lower() in a.origin_country.lower() for w in words)
    ]


def filter_by_altitude(
    aeroplanes: list[Aeroplane], altitude_range: str
) -> list[Aeroplane]:
    if not altitude_range.strip():
        return aeroplanes
    try:
        low, high = map(float, altitude_range.replace(" ", "").split("-"))
    except ValueError:
        print("Некорректный диапазон высот, пропускаем фильтр.")
        return aeroplanes
    return [a for a in aeroplanes if low <= a.altitude <= high]


def get_top_by_altitude(aeroplanes: list[Aeroplane], n: int) -> list[Aeroplane]:
    return sorted(aeroplanes, key=lambda a: a.altitude, reverse=True)[:n]


def print_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    if not aeroplanes:
        print("Самолёты не найдены.")
        return
    for a in aeroplanes:
        print(
            f"{a.callsign:>10} | {a.origin_country:<25} | "
            f"скорость: {a.velocity:>7.1f} м/с | высота: {a.altitude:>8.1f} м"
        )


def user_interaction() -> None:
    country = input("Введите название страны: ").strip()
    if not country:
        print("Страна не введена.")
        return

    try:
        top_n = int(input("Введите N для топа по высоте: "))
    except ValueError:
        print("N должно быть числом.")
        return

    filter_words = input(
        "Страны регистрации (через пробел, Enter — пропустить): "
    ).split()
    altitude_range = input("Диапазон высот (пример: 8000-12000, Enter — пропустить): ")

    try:
        api = OpenSkyAPI()
        raw = api.get_data(country)
    except (ConnectionError, ValueError) as e:
        print(f"Ошибка API: {e}")
        return

    aeroplanes = Aeroplane.cast_to_object_list(raw)
    print(f"Получено самолётов: {len(aeroplanes)}")

    saver = JSONSaver()
    for a in aeroplanes:
        saver.add_aeroplane(a)

    filtered = filter_by_country(aeroplanes, filter_words)
    ranged = filter_by_altitude(filtered, altitude_range)
    top = get_top_by_altitude(ranged, top_n)
    print_aeroplanes(top)


if __name__ == "__main__":
    user_interaction()

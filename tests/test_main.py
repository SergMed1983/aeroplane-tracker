# tests/test_main.py
from src.aeroplane import Aeroplane
from src.main import filter_by_altitude, filter_by_country, get_top_by_altitude


def test_filter_by_country():
    planes = [
        Aeroplane("A", "United States", 100, 1000),
        Aeroplane("B", "Spain", 100, 1000),
    ]
    assert len(filter_by_country(planes, ["spain"])) == 1


def test_filter_by_altitude():
    planes = [Aeroplane("A", "US", 100, 500), Aeroplane("B", "US", 100, 1500)]
    assert len(filter_by_altitude(planes, "1000-2000")) == 1


def test_top_n():
    planes = [
        Aeroplane("A", "US", 100, 500),
        Aeroplane("B", "US", 100, 1500),
        Aeroplane("C", "US", 100, 1000),
    ]
    top = get_top_by_altitude(planes, 2)
    assert [a.callsign for a in top] == ["B", "C"]


from unittest.mock import patch

from src.main import filter_by_altitude, filter_by_country, user_interaction


def test_filter_by_country_empty_words():
    planes = [Aeroplane("A", "US", 100, 1000)]
    assert filter_by_country(planes, []) == planes


def test_filter_by_altitude_empty():
    planes = [Aeroplane("A", "US", 100, 1000)]
    assert filter_by_altitude(planes, "") == planes


def test_filter_by_altitude_bad_format():
    planes = [Aeroplane("A", "US", 100, 1000)]
    assert filter_by_altitude(planes, "abc") == planes


@patch("src.main.OpenSkyAPI")
@patch("src.main.input", side_effect=["Spain", "2", "", ""])
@patch("src.main.JSONSaver")
def test_user_interaction_ok(mock_saver, mock_input, mock_api_cls):
    mock_api = mock_api_cls.return_value
    mock_api.get_data.return_value = [
        ["x", "A", "US", None, None, None, 1, 1000, False, 50],
        ["y", "B", "Spain", None, None, None, 1, 2000, False, 60],
    ]
    user_interaction()  # не должно упасть


@patch("src.main.OpenSkyAPI")
@patch("src.main.input", side_effect=["Spain", "abc", "", ""])  # N не число
def test_user_interaction_bad_n(mock_input, mock_api_cls):
    user_interaction()  # должно напечатать ошибку, но не упасть


@patch("src.main.OpenSkyAPI")
@patch("src.main.input", side_effect=["Spain", "2", "", ""])
def test_user_interaction_api_error(mock_input, mock_api_cls):
    mock_api = mock_api_cls.return_value
    mock_api.get_data.side_effect = ConnectionError("down")
    user_interaction()  # должно напечатать ошибку, но не упасть

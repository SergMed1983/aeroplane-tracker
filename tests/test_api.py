# tests/test_api.py
import pytest
import requests as real_requests
from unittest.mock import patch, MagicMock

from src.api import NominatimAPI, OpenSkyAPI

@patch("src.api.requests.get")
def test_nominatim_boundingbox(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: [{"boundingbox": ["1", "2", "3", "4"]}]
    )
    api = NominatimAPI()
    assert api.get_country_boundingbox("Spain") == ["1", "2", "3", "4"]

@patch("src.api.requests.get")
def test_opensky_data(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {"states": [["x", "A", "US", None, None, None, 1, 100, False, 50]]}
    )
    api = OpenSkyAPI()
    with patch.object(api.nominatim, "get_country_boundingbox",
                      return_value=["1", "2", "3", "4"]):
        data = api.get_data("Spain")
    assert len(data) == 1

@patch("src.api.requests.get")
def test_nominatim_connect_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200, raise_for_status=lambda: None)
    NominatimAPI().connect()  # не должно бросить исключение

@patch("src.api.requests.get")
def test_nominatim_connect_error(mock_get):
    mock_get.side_effect = real_requests.RequestException("network down")
    with pytest.raises(ConnectionError):
        NominatimAPI().connect()

@patch("src.api.requests.get")
def test_opensky_connect_ok(mock_get):
    mock_get.return_value = MagicMock(status_code=200, raise_for_status=lambda: None)
    OpenSkyAPI().connect()

@patch("src.api.requests.get")
def test_nominatim_invalid_json(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        raise_for_status=lambda: None,
        json=lambda: (_ for _ in ()).throw(ValueError("bad json"))
    )
    with pytest.raises(ValueError):
        NominatimAPI().get_data("Spain")

@patch("src.api.requests.get")
def test_opensky_no_bbox(mock_get):
    api = OpenSkyAPI()
    with patch.object(api.nominatim, "get_country_boundingbox", return_value=None):
        assert api.get_data("Spain") == []

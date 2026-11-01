# tests/test_aeroplane.py
import pytest
from src.aeroplane import Aeroplane

def test_valid_init():
    a = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
    assert a.callsign == "UAL1621"
    assert a.velocity == 268.79

@pytest.mark.parametrize("args", [
    ("", "US", 100, 100),
    ("A", "", 100, 100),
    ("A", "US", -1, 100),
    ("A", "US", 100, -1),
    ("A", "US", "fast", 100),
])
def test_invalid_init(args):
    with pytest.raises(ValueError):
        Aeroplane(*args)

def test_comparison_speed():
    a = Aeroplane("A", "US", 100, 1000)
    b = Aeroplane("B", "US", 200, 500)
    assert a < b
    assert b > a
    assert a.is_faster_than(b) is False

def test_comparison_altitude():
    a = Aeroplane("A", "US", 100, 1000)
    b = Aeroplane("B", "US", 200, 500)
    assert a.is_higher_than(b) is True

def test_cast_to_object_list():
    raw = [["abc", "UAL1621", "United States", None, None, None,
            10.0, 10203.18, False, 268.79]]
    result = Aeroplane.cast_to_object_list(raw)
    assert len(result) == 1
    assert result[0].callsign == "UAL1621"

def test_cast_empty():
    assert Aeroplane.cast_to_object_list([]) == []

def test_eq():
    a = Aeroplane("A", "US", 100, 1000)
    b = Aeroplane("A", "US", 200, 500)
    c = Aeroplane("B", "US", 100, 1000)
    assert a == b  # одинаковый callsign
    assert a != c
    assert (a == "not a plane") is False

def test_invalid_types():
    import pytest
    with pytest.raises(ValueError):
        Aeroplane(123, "US", 100, 1000)  # callsign не str
    with pytest.raises(ValueError):
        Aeroplane("A", 123, 100, 1000)   # country не str

# tests/test_saver.py
import json

from src.aeroplane import Aeroplane
from src.saver import JSONSaver


def test_add_and_get(tmp_path):
    path = tmp_path / "a.json"
    saver = JSONSaver(str(path))
    a = Aeroplane("A", "US", 100, 1000)
    saver.add_aeroplane(a)
    data = saver.get_aeroplanes()
    assert len(data) == 1 and data[0]["callsign"] == "A"


def test_delete(tmp_path):
    path = tmp_path / "a.json"
    saver = JSONSaver(str(path))
    a = Aeroplane("A", "US", 100, 1000)
    saver.add_aeroplane(a)
    saver.delete_aeroplane(a)
    assert saver.get_aeroplanes() == []


def test_get_with_criteria(tmp_path):
    path = tmp_path / "a.json"
    saver = JSONSaver(str(path))
    saver.add_aeroplane(Aeroplane("A", "US", 100, 1000))
    saver.add_aeroplane(Aeroplane("B", "Spain", 100, 1000))
    result = saver.get_aeroplanes({"origin_country": "Spain"})
    assert len(result) == 1
    assert result[0]["callsign"] == "B"


def test_broken_json(tmp_path):
    path = tmp_path / "a.json"
    path.write_text("{ not valid json", encoding="utf-8")
    saver = JSONSaver(str(path))
    assert saver.get_aeroplanes() == []

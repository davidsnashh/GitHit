import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from schemas import read_events, STATS_FIGHTER_KEYS
from stats import build_stats

FIXTURE = os.path.join(HERE, "round1_events.csv")

def load():
    return build_stats(read_events(FIXTURE))


def test_rounds():
    assert load()["rounds"] == 1


def test_red_counts():
    red = load()["fighters"]["red"]
    assert red["thrown"] == 13
    assert red["landed"] == 9
    assert red["landed_flush"] == 1


def test_blue_counts():
    blue = load()["fighters"]["blue"]
    assert blue["thrown"] == 11
    assert blue["landed"] == 6
    assert blue["landed_flush"] == 1


def test_red_accuracy():
    assert load()["fighters"]["red"]["accuracy"] == 9 / 13


def test_fighter_keys():
    fighters = load()["fighters"]
    assert list(fighters["red"]) == STATS_FIGHTER_KEYS
    assert list(fighters["blue"]) == STATS_FIGHTER_KEYS


def test_red_jab_by_strike():
    assert load()["fighters"]["red"]["by_strike"]["jab"] == {"thrown": 4, "landed": 2}


def test_blue_legs_by_target():
    assert load()["fighters"]["blue"]["by_target"]["legs"] == {"thrown": 4, "landed": 3}

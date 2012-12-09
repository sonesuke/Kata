import pytest
from Model import Game, RollService, ScoreService


def test_create():
    g = Game()


def test_roll():
    g = Game()
    RollService.roll(g, 3)


def test_invalid_roll():
    g = Game()
    with pytest.raises(Exception):
        RollService.roll(g, -1)


def test_too_many_pins_in_a_frame():
    g = Game()
    RollService.roll(g, 3)
    with pytest.raises(ValueError):
        RollService.roll(g, 8)


def test_max_frame_without_bonus():
    g = Game()
    for i in range(20):
        RollService.roll(g, 1)
    with pytest.raises(Exception):
        RollService.roll(g, 1)


def test_max_frame_with_bonus():
    g = Game()
    for i in range(21):
        RollService.roll(g, 5)
    with pytest.raises(Exception):
        RollService.roll(g, 1)


def test_calc_score():
    g = Game()
    assert ScoreService.calculate(g) == 0
    RollService.roll(g, 3)
    assert ScoreService.calculate(g) == 3


def test_calc_all_strike():
    g = Game()
    for i in range(12):
        RollService.roll(g, 10)
    assert ScoreService.calculate(g) == 300


def test_calc_all_spare():
    g = Game()
    for i in range(21):
        RollService.roll(g, 5)
    assert ScoreService.calculate(g) == 150

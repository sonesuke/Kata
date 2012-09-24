import pytest
from Kata import Game


def test_create():
    g = Game()


def test_roll():
    g = Game()
    g.roll(3)
    assert g.calc_score() == 3


def test_over_pins_in_a_roll():
    g = Game()
    with pytest.raises(ValueError):
        g.roll(11)
    with pytest.raises(ValueError):
        g.roll(-1)


def test_spare():
    g = Game()
    g.roll(3)
    g.roll(7)
    g.roll(3)
    g.roll(2)
    assert g.calc_score() == 18


def test_strike():
    g = Game()
    g.roll(10)
    g.roll(7)
    g.roll(2)
    g.roll(2)
    assert g.calc_score() == 30


def test_over_pins_in_a_frame():
    g = Game()
    g.roll(3)
    with pytest.raises(ValueError):
        g.roll(8)


def test_complete():
    g = Game()
    for i in range(12):
        g.roll(10)
    assert g.calc_score() == 300

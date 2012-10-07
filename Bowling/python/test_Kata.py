#14:16
import pytest
from Kata import Game


def test_create():
    g = Game()


def test_roll():
    g = Game()
    g.roll(3)


def test_roll_error():
    g = Game()
    with pytest.raises(ValueError):
        g.roll(-1)


def test_pins_over_in_a_frame():
    g = Game()
    g.roll(3)
    with pytest.raises(ValueError):
        g.roll(8)


def test_frames_over():
    g = Game()
    for i in range(20):
        g.roll(0)
    with pytest.raises(ValueError):
        g.roll(0)


def test_last_frame():
    g = Game()
    for i in range(18):
        g.roll(0)
    g.roll(10)
    g.roll(10)
    g.roll(10)


def test_pins_over_in_last_frame():
    g = Game()
    for i in range(18):
        g.roll(0)
    g.roll(3)
    with pytest.raises(ValueError):
        g.roll(8)


def test_score():
    g = Game()
    assert g.calc_score() == 0
    g.roll(3)
    assert g.calc_score() == 3


def test_spare():
    g = Game()
    g.roll(3)
    g.roll(7)
    g.roll(3)
    g.roll(3)
    assert g.calc_score() == 19


def test_strike():
    g = Game()
    g.roll(10)
    g.roll(7)
    g.roll(2)
    g.roll(3)
    assert g.calc_score() == 31


def test_complete():
    g = Game()
    for i in range(12):
        g.roll(10)
    assert g.calc_score() == 300


def test_all_spare():
    g = Game()
    for i in range(21):
        g.roll(5)
    assert g.calc_score() == 150

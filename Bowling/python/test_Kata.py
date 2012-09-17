import pytest
from Kata import Game


def test_create():
    g = Game()


def test_roll():
    g = Game()
    g.roll(3)
    assert g.score == 3


def test_pins_10_over():
    g = Game()
    with pytest.raises(ValueError):
        g.roll(11)
    with pytest.raises(ValueError):
        g.roll(3)
        g.roll(8)


def test_spare():
    g = Game()
    g.roll(3)
    g.roll(7)
    g.roll(2)
    g.roll(1)
    assert g.score == 15


def test_strike():
    g = Game()
    g.roll(10)
    g.roll(7)
    g.roll(2)
    g.roll(1)
    assert g.score == 29


def test_complete():
    g = Game()
    for i in range(12):
        g.roll(10)
    assert g.score == 300


def test_all_spare():
    g = Game()
    for i in range(21):
        g.roll(5)
    assert g.score == 150


def test_frame_10_over():
    g = Game()
    for i in range(20):
        g.roll(0)
    with pytest.raises(ValueError):
        g.roll(0)


def test_frame_10_error_case1():
    g = Game()
    for i in range(18):
        g.roll(0)
    with pytest.raises(ValueError):
        g.roll(9)
        g.roll(2)


def test_frame_10_error_case2():
    g = Game()
    for i in range(18):
        g.roll(0)
    g.roll(10)
    with pytest.raises(ValueError):
        g.roll(2)
        g.roll(9)

import pytest
from Kata import Game


def test_create():
    g = Game()


def test_roll():
    g = Game()
    g.roll(3)
    assert g.calc_score() == 3


def test_roll_over():
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


def test_rolls_over_in_frame():
    g = Game()
    g.roll(3)
    with pytest.raises(ValueError):
        g.roll(8)


def test_complete():
    g = Game()
    for i in range(12):
        g.roll(10)
    assert g.calc_score() == 300


def test_all_5():
    g = Game()
    for i in range(21):
        g.roll(5)
    assert g.calc_score() == 150


def test_10_frame_error1():
    g = Game()
    for i in range(18):
        g.roll(0)
    g.roll(3)
    with pytest.raises(ValueError):
        g.roll(8)


def test_10_frame_error2():
    g = Game()
    for i in range(18):
        g.roll(0)
    g.roll(3)
    g.roll(7)
    with pytest.raises(ValueError):
        g.roll(4)


def test_10_frame_error3():
    g = Game()
    for i in range(18):
        g.roll(0)
    g.roll(10)
    g.roll(7)
    with pytest.raises(ValueError):
        g.roll(4)


def test_10_frame_over1():
    g = Game()
    for i in range(20):
        g.roll(0)
    with pytest.raises(ValueError):
        g.roll(0)


def test_10_frame_over2():
    g = Game()
    for i in range(12):
        g.roll(10)
    with pytest.raises(ValueError):
        g.roll(0)

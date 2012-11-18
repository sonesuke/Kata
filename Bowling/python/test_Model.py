#930 10:11
import pytest
from Model import Game


def test_create():
    g = Game()


def test_roll():
    g = Game()
    g.roll(3)


def test_raise_exception_by_invalid_roll():
    g = Game()
    with pytest.raises(ValueError):
        g.roll(-1)


def test_raise_exception_by_pins_over_in_a_frame():
    g = Game()
    g.roll(3)
    with pytest.raises(ValueError):
        g.roll(8)


def test_raise_exception_by_frames_over():
    g = Game()
    for i in range(20):
        g.roll(0)
    with pytest.raises(ValueError):
        g.roll(0)


def test_count_of_last_frame():
    g = Game()
    for i in range(12):
        g.roll(10)

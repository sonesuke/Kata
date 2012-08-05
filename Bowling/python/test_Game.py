import pytest
from Game import Game


def test_create():
    g = Game()


def test_roll():
    g = Game()
    g.roll(3)
    with pytest.raises(ValueError):
        g.roll(8)
    g.roll(4)
    with pytest.raises(ValueError):
        g.roll(11)


def test_score():
    g = Game()
    assert g.score == 0
    g.roll(3)
    assert g.score == 3


def test_spare():
    g = Game()
    g.roll(3)
    g.roll(7)
    g.roll(5)
    g.roll(3)
    assert g.score == 23


def test_strike():
    g = Game()
    g.roll(10)
    g.roll(3)
    g.roll(5)
    g.roll(3)
    assert g.score == 29


@pytest.mark.parametrize(
    ('rolls', 'expected'),
    [
        ([1, 2], 18 + 3),
        ([10, 5, 5], 18 + 30),
        ([5, 5, 10], 18 + 30),
    ]
)
def test_10_frame(rolls, expected):
    g = Game()
    for i in range(0, 18):
        g.roll(1)

    for r in rolls:
        g.roll(r)
    assert g.score == expected
    with pytest.raises(ValueError):
        g.roll(1)


def test_10_frame_error():
    g = Game()
    for i in range(0, 18):
        g.roll(1)

    with pytest.raises(ValueError):
        g.roll(11)


def test_10_frame_2nd_roll():
    g = Game()
    for i in range(0, 18):
        g.roll(1)
    g.roll(2)
    with pytest.raises(ValueError):
        g.roll(9)

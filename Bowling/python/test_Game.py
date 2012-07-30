import pytest
from Game import Game


def test_craete():
    g = Game()
    assert g


def test_roll():
    g = Game()
    g.roll(3)


def test_spare():
    g = Game()
    g.roll(0)
    g.roll(1)
    g.roll(2)
    g.roll(8)
    g.roll(4)
    g.roll(5)
    assert g.frame() == [[0, 1], [2, 8], [4, 5]]
    assert g.score() == 1 + 10 + 4 + 9


@pytest.mark.parametrize(("input", "frame_expected", "score_expetected"), [
    ([1, 2, 3, 4, 5], [[1, 2], [3, 4], [5]], 1 + 2 + 3 + 4 + 5), # normal case
    ([10, 1, 2, 3, 4, 5], [[10], [1, 2], [3, 4], [5]], 10 + 3 + 3 + 7 + 5), # one strike
    ([10, 1, 2, 10, 10, 5], [[10], [1, 2], [10], [10], [5]], 10 + 3 + 3 + 10 + 10 + 10 + 5 + 5), # two strike
    ([0, 1, 2, 8, 4, 5], [[0, 1], [2, 8], [4, 5]], 1 + 10 + 4 + 9),
])
def test_frame(input, frame_expected, score_expetected):
    g = Game()
    for i in input:
        g.roll(i)
    assert g.frame() == frame_expected
    assert g.score() == score_expetected


def test_frames_over():
    g = Game()
    for i in range(0, 9):
        g.roll(1)
        g.roll(1)
    g.roll(1)
    g.roll(1)
    with pytest.raises(ValueError):
        g.roll(1)


def test_score():
    g = Game()
    assert g.score() == 0
    g.roll(3)
    assert g.score() == 3


def test_roll_ten_over():
    g = Game()
    with pytest.raises(ValueError):
        g.roll(11)


def test_frame_ten_over():
    g = Game()
    g.roll(3)
    with pytest.raises(ValueError):
        g.roll(8)


def test_10_frame():
    g = Game()
    for idx in range(0, 9):
        g.roll(1)
        g.roll(1)
    g.roll(10)
    g.roll(2)
    g.roll(3)
    print g.frame()
    assert g.frame()[-1] == [10, 2, 3]
    assert g.score() == 2 * 9 + 10 + 5 + 5

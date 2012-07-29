
from Kata import Game
from nose.tools import ok_, eq_, raises


def test_craete():
    g = Game()
    ok_(g)


def test_roll():
    g = Game()
    g.roll(3)


def test_frame():
    g = Game()
    g.roll(1)
    g.roll(2)
    g.roll(3)
    g.roll(4)
    g.roll(5)
    eq_(g.frame(), [[1, 2], [3, 4], [5]])


@raises(ValueError)
def test_frames_over():
    g = Game()
    for i in range(0, 9):
        g.roll(1)
        g.roll(1)
    g.roll(1)
    g.roll(1)
    g.roll(1)


def test_score():
    g = Game()
    eq_(g.score(), 0)
    g.roll(3)
    eq_(g.score(), 3)


@raises(ValueError)
def test_roll_ten_over():
    g = Game()
    g.roll(11)


@raises(ValueError)
def test_frame_ten_over():
    g = Game()
    g.roll(3)
    g.roll(8)


def test_strike():
    g = Game()
    g.roll(10)
    g.roll(1)
    g.roll(2)
    g.roll(3)
    g.roll(4)
    g.roll(5)
    eq_(g.frame(), [[10], [1, 2], [3, 4], [5]])
    eq_(g.score(), 10 + 3 + 3 + 7 + 5)


def test_two_strike():
    g = Game()
    g.roll(10)
    g.roll(1)
    g.roll(2)
    g.roll(10)
    g.roll(10)
    g.roll(5)
    eq_(g.frame(), [[10], [1, 2], [10], [10], [5]])
    eq_(g.score(), 10 + 3 + 3 + 10 + 10 + 10 + 5 + 5)


def test_spare():
    g = Game()
    g.roll(0)
    g.roll(1)
    g.roll(2)
    g.roll(8)
    g.roll(4)
    g.roll(5)
    eq_(g.frame(), [[0, 1], [2, 8], [4, 5]])
    eq_(g.score(), 1 + 10 + 4 + 9)


def test_10_frame():
    g = Game()
    for idx in range(0, 9):
        g.roll(1)
        g.roll(1)
    g.roll(10)
    g.roll(2)
    g.roll(3)
    print g.frame()
    eq_(g.frame()[-1], [10, 2, 3])
    eq_(g.score(), 2 * 9 + 10 + 5 + 5)

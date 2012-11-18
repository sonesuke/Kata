import pytest
from Model import Game
from ScoreService import Scorer


def test_score():
    g = Game()
    assert Scorer.calc_score(g.frames) == 0
    g.roll(3)
    assert Scorer.calc_score(g.frames) == 3


def test_spare():
    g = Game()
    for i in range(21):
        g.roll(5)
    assert Scorer.calc_score(g.frames) == 150


def test_strike():
    g = Game()
    for i in range(12):
        g.roll(10)
    assert Scorer.calc_score(g.frames) == 300

import pytest
from Model import Game, RollService
from DrawService import DrawService
from unittest.mock import Mock, call


def test_create():
    dc = Mock()
    d = DrawService(dc)


def test_draw_index():
    g = Game()
    for i in range(5):
        RollService.roll(g, 3)
    dc = Mock()
    d = DrawService(dc)
    d.draw(g)
    assert dc.draw_index.call_count == 3


def test_draw_pins():
    g = Game()
    for i in range(5):
        RollService.roll(g, i)
    dc = Mock()
    d = DrawService(dc)
    d.draw(g)
    assert dc.draw_pins.call_count == 5


def test_draw_spare_pins():
    g = Game()
    RollService.roll(g, 2)
    RollService.roll(g, 8)
    dc = Mock()
    d = DrawService(dc)
    d.draw(g)
    assert dc.draw_pins.call_args_list[0] == call(2)
    assert dc.draw_spare.call_count == 1


def test_draw_strike_pins():
    g = Game()
    RollService.roll(g, 10)
    dc = Mock()
    d = DrawService(dc)
    d.draw(g)
    assert dc.draw_strike.call_args_list[0] == call()


def test_draw_score():
    g = Game()
    for i in range(5):
        RollService.roll(g, i)
    dc = Mock()
    d = DrawService(dc)
    d.draw(g)
    assert dc.draw_score.call_count == 3
    assert dc.draw_score.call_args_list[0] == call(1)
    assert dc.draw_score.call_args_list[1] == call(6)
    assert dc.draw_score.call_args_list[2] == call(10)


def test_draw_flush():
    g = Game()
    dc = Mock()
    d = DrawService(dc)
    d.draw(g)
    assert dc.flush.call_count == 1

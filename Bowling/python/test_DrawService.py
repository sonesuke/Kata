import pytest
from Model import Game
from DrawService import DrawService
from unittest.mock import Mock, call


def test_create():
    dc = Mock()
    d = DrawService(dc)


def test_draw_frame_no():
    g = Game()
    for i in range(5):
        g.roll(3)
    dc = Mock()
    d = DrawService(dc)
    d.draw(g)
    assert dc.draw_frame_no.call_count == 1
    assert dc.draw_frame_no.call_args == call(3)


def test_draw_pins():
    g = Game()
    for i in range(5):
        g.roll(i)
    dc = Mock()
    d = DrawService(dc)
    d.draw(g)
    assert dc.draw_pins.call_count == 3
    assert dc.draw_pins.call_args_list[0] == call(['0', '1'])
    assert dc.draw_pins.call_args_list[1] == call(['2', '3'])
    assert dc.draw_pins.call_args_list[2] == call(['4'])


def test_draw_spare_pins():
    g = Game()
    g.roll(2)
    g.roll(8)
    dc = Mock()
    d = DrawService(dc)
    d.draw(g)
    assert dc.draw_pins.call_args_list[0] == call(['2', '/'])


def test_draw_strike_pins():
    g = Game()
    g.roll(10)
    dc = Mock()
    d = DrawService(dc)
    d.draw(g)
    assert dc.draw_pins.call_args_list[0] == call(['X', ''])


def test_draw_score():
    g = Game()
    for i in range(5):
        g.roll(i)
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

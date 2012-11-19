import pytest
from Console import Console


def test_create():
    c = Console()


def test_draw_frame_no():
    c = Console()
    c.draw_frame_no(5)
    assert c.frame_no_line == '     1     2     3     4     5'


def test_draw_pins():
    c = Console()
    c.draw_pins(['1', '2', '3', '4'])
    assert c.pins_line == '  1  2  3  4'


def test_draw_score():
    c = Console()
    c.draw_score(5)
    assert c.score_line == '     5'

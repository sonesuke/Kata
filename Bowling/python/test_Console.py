import pytest
from Console import Console


def test_create():
    c = Console()


def test_draw_frame_no():
    c = Console()
    for i in range(5):
        c.draw_index(i + 1)
    assert c.frame_no_line == '     1     2     3     4     5'


def test_draw_pins():
    c = Console()
    for i in range(4):
        c.draw_pins(i + 1)
    assert c.pins_line == '  1  2  3  4'


def test_draw_score():
    c = Console()
    c.draw_score(5)
    assert c.score_line == '     5'


def test_draw_spare():
    c = Console()
    for i in range(4):
        c.draw_spare()
    assert c.pins_line == '  /  /  /  /'


def test_draw_stirke():
    c = Console()
    for i in range(4):
        c.draw_strike()
    assert c.pins_line == '  X  X  X  X'


def test_draw_blank():
    c = Console()
    for i in range(4):
        c.draw_blank()
    assert c.pins_line == '            '

import pytest
from unittest.mock import Mock, call
from Domain import Game
from Application import SaveService, LoadService


def test_create_save_service():
    archive = Mock()
    s = SaveService(archive)


def test_save():
    archive = Mock()
    g = Game()
    g.roll(3)
    s = SaveService(archive)
    s.save(g)
    assert archive.write_header.call_count == 5
    assert archive.write_footer.call_count == 5
    assert archive.write_count.call_args == call(1)
    assert archive.write_body.call_args == call(3)


def test_create_load_service():
    archive = Mock()
    s = SaveService(archive)


def test_load():
    archive = Mock()
    archive.load_count.return_value = 1
    archive.load_body.return_value = 3
    l = LoadService(archive)
    g = l.load()
    assert g.calc_score() == 3

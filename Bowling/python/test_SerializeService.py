import pytest
from unittest.mock import Mock, call, patch
from Model import Game, RollService, ScoreService
from SerializeService import SaveService, LoadService


def test_create_save_service():
    stream = Mock()
    s = SaveService(stream)


def test_save():
    stream = Mock()
    g = Game()
    RollService.roll(g, 3)
    SaveService(stream).save(g)
    assert stream.write_header.call_count == 5
    assert stream.write_footer.call_count == 5
    assert stream.write_count.call_args == call(1)
    assert stream.write_body.call_args == call(3)


def test_create_load_service():
    stream = Mock()
    s = SaveService(stream)


def test_load():
    stream = Mock()
    stream.load_count.return_value = 1
    stream.load_body.return_value = 3
    with patch('SerializeService.Unpack') as m:
        m.__enter__.return_value = True
        g = LoadService(stream).load()
    assert ScoreService.calculate(g) == 3

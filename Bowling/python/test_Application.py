import pytest
import mock
from Domain import Game
from Application import SaveService


def test_create():
    archive = mock.Mock()
    s = SaveService(archive)


def test_save():
    archive = mock.Mock()
    g = Game()
    s = SaveService(archive)
    s.save(g)
    assert archive.write_header.call_args_list[0] == mock.call('game')
    assert archive.write_header.call_args_list[1] == mock.call('frames')
    assert archive.write_header.call_args_list[2] == mock.call('frame')
    assert archive.write_header.call_args_list[3] == mock.call('rolls')
    assert archive.write_footer.call_args_list[0] == mock.call('rolls')
    assert archive.write_footer.call_args_list[1] == mock.call('frame')
    assert archive.write_footer.call_args_list[2] == mock.call('frames')
    assert archive.write_footer.call_args_list[3] == mock.call('game')


def test_load():
    pass
